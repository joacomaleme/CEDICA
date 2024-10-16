from uuid import uuid4
from flask import redirect, request, send_file, abort, url_for
from minio import Minio  # Assuming you're using the MinIO client
from src.model.generic.operations import document_operations
from flask import Blueprint, current_app

bp = Blueprint("document", __name__, url_prefix="/document")

@bp.post('/create')
def create():
    employee_id = request.form.get('employee_id')
    rider_id = request.form.get('rider_id')

    if "files" in request.files:
        files = request.files.getlist("files")

        # Tomo el cliente
        client = current_app.storage.client

        for file in files:
            filename = remove_extension(file.filename)
            path = f"{uuid4()}-{file.filename}" # Uso uuid4() para generar un número random y que no se repita el nombre
            content_type = file.content_type

            document_operations.create_document(title=filename, format=f"{content_type}", is_external=False, allowed_operations="",
                                                file_address=path, employee_id=employee_id, rider_id=rider_id)

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
        document_operations.delete_document(document_id)

        # Return success or redirect to the document list
        return redirect(request.referrer)

    except Exception as e:
        return abort(500, description="Ocurrio un error intentando eliminar el documento.")

def remove_extension(path: str) -> str:
    split = path.split(".")
    return ".".join(split[:-1]) if len(split) > 1 else path