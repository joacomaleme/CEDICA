from src.model.database import db
from src.model.horses.tables.horse import Horse
from sqlalchemy.orm  import Query
from typing import Optional, List, Tuple
from src.model.generic.operations.work_proposal_operations import search_name

def create_horse(name, birth, sex, breed, coat, is_donated, sede_id, active, activity_id) -> Horse:
    horse = Horse(name=name, birth=birth, sex=sex, breed=breed, coat=coat, is_donated=is_donated, sede_id=sede_id, active=active, activity_id=activity_id)
    db.session.add(horse)
    db.session.commit()
    db.session.expunge(horse)
    return horse


def get_horse(horse_id: int) -> Optional[Horse]:
    horse = Horse.query.get(horse_id)
    if horse:
        db.session.expunge(horse)
    return horse


def list_horses() -> List[Horse]:
    horses = Horse.query.all()
    [db.session.expunge(horse) for horse in horses]
    return horses


def update_horse(to_update: Horse) -> Horse:
    horse = Horse.query.get(to_update.id)
    if horse is None:
        raise ValueError("No se encontro un caballo con ese ID")
    horse.name = to_update.name or horse.name
    horse.birth = to_update.birth or horse.birth
    horse.sex = to_update.sex if to_update.sex is not None else horse.sex
    horse.breed = to_update.breed or horse.breed
    horse.coat = to_update.coat or horse.coat
    horse.is_donated = to_update.is_donated if to_update.is_donated is not None else horse.is_donated
    horse.sede_id = to_update.sede_id or horse.sede_id
    horse.active = to_update.active if to_update.active is not None else horse.active
    horse.activity_id = to_update.activity_id or horse.activity_id
    db.session.commit()
    db.session.expunge(horse)
    return horse


def delete_horse(horse_id: int):
    horse = Horse.query.get(horse_id)
    if horse is None:
        raise ValueError("No se encontro un caballo con ese ID")
    db.session.delete(horse)
    db.session.commit()


# Ordena por un atributo específico (name por defecto)
def sorted_by_attribute(horses: Query, attribute: str = "name", ascending: bool = True) -> Query:
    return horses.order_by(getattr(Horse, attribute).asc() if ascending else getattr(Horse, attribute).desc())

# Búsqueda por nombre o tipo de J&A asignados
def search_by_attribute(horses: Query, search_attr: str = "name", search_value: str = "") -> Query:
    match search_attr:
        case "name":
            return horses.filter(Horse.name.ilike(f"%{search_value}%"))
        case "assigned_type":
            return horses.filter(Horse.activity.name.ilike(f"%{search_value}%"))
        case _:
            return horses

def filter_by_activity(horses: Query, activity_name: str = "") -> Query:
    activity = search_name(activity_name)
    if activity:
        return horses.filter(db.and_(Horse.activity_id.isnot(None), Horse.activity_id == activity.id))
    else:
        return horses

# Función final que combina los filtros y búsquedas
def get_horses_filtered_list(page: int,
                             limit: int = 25,
                             sort_attr: str = "name",
                             ascending: bool = True,
                             activity: str = "",
                             search_attr: str = "name",
                             search_value: str = "") -> Tuple[Horse, int]:
    # Inicia la consulta con Horse
    horses = Horse.query
    
    # Aplica los filtros y búsquedas
    horses = search_by_attribute(horses, search_attr, search_value)
    horses = filter_by_activity(horses, activity)
    # Ordena los resultados
    horses = sorted_by_attribute(horses, sort_attr, ascending)
    
    # Pagina los resultados
    horse_list = horses.paginate(page=page, per_page=limit, error_out=False)
    
    # Expulsa los objetos de la sesión
    [db.session.expunge(horse) for horse in horse_list.items]
    
    return (horse_list, ((horses.count()-1)//limit)+1)
