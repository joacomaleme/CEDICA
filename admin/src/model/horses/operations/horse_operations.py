from src.model.database import db
from src.model.horses.tables.horse import Horse
from sqlalchemy.orm  import Query
from typing import Optional, List

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
    horse.sex = to_update.sex or horse.sex
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


# Ordena por un atributo específico (nombre por defecto)
def sorted_by_attribute(horses: Query, attribute: str = "name", ascending: bool = True) -> Query:
    return horses.order_by(getattr(Horse, attribute).asc() if ascending else getattr(Horse, attribute).desc())

# Búsqueda por nombre
def search_by_name(horses: Query, name: str = "") -> Query:
    if name:
        return horses.filter(Horse.name.ilike(f"%{name}%"))
    return horses

# Búsqueda por Tipo de J&A Asignados
def search_by_assigned_type(horses: Query, assigned_type: str = "") -> Query:
    if assigned_type:
        return horses.filter(Horse.activity.name.ilike(f"%{assigned_type}%"))
    return horses

# Función final que combina los filtros y búsquedas
def get_horses_filtered_list(page: int,
                             limit: int = 25,
                             sort_attr: str = "name",
                             ascending: bool = True,
                             search_name: str = "",
                             search_assigned_type: str = "") -> Query:
    ## Tener en cuenta que profesional que lo atiende es TEXT
    # Inicia la consulta con Horse
    horses = Horse.query

    # Aplica los filtros y búsquedas
    horses = search_by_name(horses, search_name)
    horses = search_by_assigned_type(horses, search_assigned_type)

    # Ordena los resultados
    horses = sorted_by_attribute(horses, sort_attr, ascending)

    # Pagina los resultados
    horse_list = horses.paginate(page=page, per_page=limit, error_out=False)

    # Expulsa los objetos de la sesión
    [db.session.expunge(horse) for horse in horse_list.items]

    return horse_list
