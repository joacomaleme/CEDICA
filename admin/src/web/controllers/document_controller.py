import tempfile
from typing import Optional, Tuple
from uuid import uuid4
from flask import redirect, request, send_file, abort, flash, Blueprint, current_app
from src.model.generic.operations import document_operations
from src.model.generic.operations import document_types_operations
from model.horses.operations import horse_document_operations
from model.riders.operations import rider_document_operations
from src.model.employees.operations import employee_document_operations

bp = Blueprint("document", __name__, url_prefix="/document")

@bp.post('/create')
def create():
    relation = request.form.get('relation')
    id = request.form.get('id')

    if "files" in request.files and id is not None:
        files = request.files.getlist("files")

        # Tomo el cliente
        client = current_app.storage.client


        for file in files:
            filename = remove_extension(file.filename)
            path = f"{uuid4()}-{file.filename}" # Uso uuid4() para generar un número random y que no se repita el nombre
            content_type = file.content_type

            if len(filename) > 512 or len(path) > 512:
                flash("Nombre del archivo demasiado largo.", "error")
                return redirect(request.referrer)

            # Tomo el tamaño del archivo
            file_content = file.read()
            size = len(file_content)
            file.seek(0)
            # Subo a MINIO
            try:
                client.put_object("grupo03", path, file.stream, size, content_type=content_type)
            except:
                flash("El servidor esta teniendo problemas para realizar esta accion en este momento, intente mas tarde.", "error")
                return redirect(request.referrer)
            # Creo el documento en la bd
            document = document_operations.create_document(title=filename, format=f"{content_type}", is_external=False, allowed_operations="", file_address=path)

            if relation == "employee":
                employee_document_operations.create_employee_document(int(id), document.id)
            elif relation == "horse":
                horse_document_operations.create_horse_document(int(id), document.id)
            elif relation == "rider":
                rider_document_operations.create_horse_document(int(id), document.id)
            else:
                return abort(400, description="No files uploaded.")


    else:
        return abort(400, description="No files uploaded.")

    return redirect(request.referrer)

@bp.post('/linkcreate')
def link_create():
    params = request.form

    relation = params.get('relation')
    id = params.get('id')

    title = params.get('title')
    type = params.get('type')
    format = params.get('format')
    file_address = params.get('file_address')

    res = check_link_data(id, relation, title, type, format, file_address)
    if res[0] is False:
        flash(res[1], "error")
        return redirect(request.referrer)

    type = document_types_operations.get_document_type_by_name(type)

    if not type:
        flash("El tipo ingresado es inválido.", "error")
        return redirect(request.referrer)

    document = document_operations.create_document(title=title, format=format, is_external=True, allowed_operations="",
                                                   file_address=file_address, type_id=type.id)

    if relation == "employee":
        employee_document_operations.create_employee_document(int(id), document.id)
    elif relation == "horse":
        horse_document_operations.create_horse_document(int(id), document.id)
    elif relation == "rider":
        rider_document_operations.create_horse_document(int(id), document.id)
    else:
        return abort(400, description="No files uploaded.")

    return redirect(request.referrer)

@bp.route('/download/<int:document_id>')
def download(document_id: int):
    document = document_operations.get_document(document_id)

    if not document:
        return abort(404)

    if not document.is_external:
        try:
            bucket_name = "grupo03"
            object_name = document.file_address

            # Descargo el archivo de MinIO
            try:
                minio_client = current_app.storage.client
                response = minio_client.get_object(bucket_name, object_name)
                data = response.read()
                
                # Guardar el archivo temporalmente
                with tempfile.NamedTemporaryFile(delete=False) as temp_file:
                    temp_file.write(data)
                    temp_file_path = temp_file.name

            except Exception as e:
                flash("El servidor está teniendo problemas para realizar esta acción en este momento, intente más tarde.", "error")
                return redirect(request.referrer)

            # Retornar el archivo temporal como descarga
            return send_file(
                temp_file_path,
                download_name=document.file_address,
                as_attachment=True
            )
        except Exception as e:
            abort(500)

    return abort(403)

@bp.post('/destroy/<int:document_id>')
# @permissions_required(['employee_document', 'horse_document', 'rider_document'])
def destroy(document_id: int):
    document = document_operations.get_document(document_id)
    relation = request.form.get("relation")

    if not document:
        return abort(404, description="Documento no encontrado.")

    if relation != "employee" and relation != "horse" and relation != "rider":
        return abort(404, description="Parámetro inválido.")

    try:
        # Si el documento no es externo lo remuevo de minio
        if not document.is_external:
            bucket_name = "grupo03"
            object_name = document.file_address

            try:
                minio_client = current_app.storage.client
                minio_client.remove_object(bucket_name, object_name)
            except:
                flash("El servidor esta teniendo problemas para realizar esta accion en este momento, intente mas tarde.", "error")
                return redirect(request.referrer)

        # Lo elimino de la db
        if relation == "employee":
            employee_document_operations.delete_employee_document(document_id)
        elif relation == "horse":
            horse_document_operations.delete_horse_document(document_id)
        elif relation == "rider":
            rider_document_operations.delete_rider_document(document_id)

        # Return success or redirect to the document list
        return redirect(request.referrer)

    except Exception as e:
        print(e)
        return abort(500, description="Ocurrio un error intentando eliminar el documento.")

def remove_extension(path: str) -> str:
    split = path.split(".")
    return ".".join(split[:-1]) if len(split) > 1 else path

def check_link_data(id: Optional[str], relation: Optional[str], title: Optional[str], type: Optional[str], format: Optional[str], file_address: Optional[str]) -> Tuple[bool, str]:
    if not id or not relation or not title or not type or not format or not file_address:
        return (False, "Todos los campos son obligatorios.")
    if not isinstance(id, str) or not isinstance(relation, str) or not isinstance(title, str) or not isinstance(type, str) or not isinstance(format, str) or not isinstance(file_address, str):
        return (False, "Algúno de los tipos de los parámetros es incorrecto.")
    if len(title) > 512 or len(file_address) > 512:
        return (False, "Nombre del archivo demasiado largo.")
    if relation != "employee" or relation != "horse" or relation != "rider":
        return (False, "Parámetro relation inválido.")
    
    return (True, "")
