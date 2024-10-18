from uuid import uuid4
from flask import redirect, request, send_file, abort, url_for
from minio import Minio
from model.horses.operations import horse_document_operations
from model.riders.operations import rider_document_operations
from src.model.generic.operations import document_operations
from src.model.employees.operations import employee_documents_operations
from flask import Blueprint, current_app

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

            document = document_operations.create_document(title=filename, format=f"{content_type}", is_external=False, allowed_operations="", file_address=path)

            if relation == "employee":
                employee_documents_operations.create_employee_document(int(id), document.id)
            elif relation == "horse":
                horse_document_operations.create_horse_document(int(id), document.id)
            elif relation == "rider":
                rider_document_operations.create_horse_document(int(id), document.id)
            else:
                return abort(400, description="No files uploaded.")

            # Tomo el tamaño del archivo
            file_content = file.read()
            size = len(file_content)
            file.seek(0)

            # Subo a MINIO
            client.put_object("grupo03", path, file.stream, size, content_type=content_type)
    else:
        return abort(400, description="No files uploaded.")

    return redirect(request.referrer)

@bp.route('/download/<int:document_id>')
def download(document_id: int):
    document = document_operations.get_document(document_id)

    if not document:
        return abort(404)

    # Si is_external=False entonces está en minio
    if not document.is_external:
        try:
            bucket_name = "grupo03"
            object_name = document.file_address

            # Descargo el archivo de minio
            minio_client = current_app.storage.client

            response = minio_client.get_object(bucket_name, object_name)

            # Retorno el archivo como descarga
            return send_file(
                response,
                download_name=document.file_address,
                as_attachment=True
            )
        except Exception as e:
            abort(500)

    return abort(403)

@bp.post('/destroy/<int:document_id>')
def destroy(document_id: int):
    document = document_operations.get_document(document_id)
    relation = request.form.get('relation')

    if not document:
        return abort(404, description="Documento no encontrado.")

    try:
        # Si el documento no es externo lo remuevo de minio
        if not document.is_external:
            bucket_name = "grupo03"
            object_name = document.file_address

            minio_client = current_app.storage.client

            minio_client.remove_object(bucket_name, object_name)

        # Lo elimino de la db
        if relation == "employee":
            employee_documents_operations.delete_employee_document(document_id)
        elif relation == "horse":
            horse_document_operations.delete_employee_document(document.id)
        elif relation == "rider":
            rider_document_operations.delete_employee_document(document.id)
        else:
            return abort(400, description="No files uploaded.")

        # Return success or redirect to the document list
        return redirect(request.referrer)

    except Exception as e:
        print(e)
        return abort(500, description="Ocurrio un error intentando eliminar el documento.")

def remove_extension(path: str) -> str:
    split = path.split(".")
    return ".".join(split[:-1]) if len(split) > 1 else path