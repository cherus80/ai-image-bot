"""
Сервис валидации файлов.

Проверяет MIME-тип, размер, magic bytes (сигнатуры файлов).
"""

import imghdr
from typing import Optional

from fastapi import UploadFile, HTTPException, status

from app.core.config import settings


# Magic bytes для различных форматов изображений
IMAGE_SIGNATURES = {
    'jpeg': [
        bytes([0xFF, 0xD8, 0xFF, 0xE0]),  # JFIF
        bytes([0xFF, 0xD8, 0xFF, 0xE1]),  # EXIF
        bytes([0xFF, 0xD8, 0xFF, 0xDB]),  # JPEG RAW
    ],
    'png': [bytes([0x89, 0x50, 0x4E, 0x47, 0x0D, 0x0A, 0x1A, 0x0A])],
}


class FileValidationError(Exception):
    """Ошибка валидации файла"""
    pass


async def validate_image_file(file: UploadFile) -> bool:
    """
    Валидация загруженного изображения.

    Проверяет:
    - MIME-тип
    - Размер файла
    - Magic bytes (сигнатура файла)

    Args:
        file: Загруженный файл

    Returns:
        bool: True если файл валиден

    Raises:
        HTTPException: Если файл не проходит валидацию
    """
    # Проверка MIME-типа
    if not file.content_type:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="File content type is missing"
        )

    allowed_mime_types = ['image/jpeg', 'image/jpg', 'image/png']
    if file.content_type not in allowed_mime_types:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid file type. Allowed types: {', '.join(allowed_mime_types)}"
        )

    # Чтение файла для проверки
    content = await file.read()
    file_size = len(content)

    # Возвращаем указатель в начало файла
    await file.seek(0)

    # Проверка размера
    max_size = settings.MAX_FILE_SIZE_BYTES
    if file_size > max_size:
        raise HTTPException(
            status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
            detail=f"File too large. Maximum size: {settings.MAX_FILE_SIZE_MB}MB"
        )

    if file_size == 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="File is empty"
        )

    # Проверка magic bytes (сигнатуры файла)
    is_valid_signature = False

    # Проверяем JPEG
    for jpeg_sig in IMAGE_SIGNATURES['jpeg']:
        if content.startswith(jpeg_sig):
            is_valid_signature = True
            break

    # Проверяем PNG
    if not is_valid_signature and content.startswith(IMAGE_SIGNATURES['png'][0]):
        is_valid_signature = True

    if not is_valid_signature:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid image file signature"
        )

    # Дополнительная проверка через imghdr
    try:
        # Возвращаемся в начало для imghdr
        await file.seek(0)
        image_type = imghdr.what(file.file)

        if image_type not in ['jpeg', 'png']:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid image format detected"
            )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Failed to validate image: {str(e)}"
        )
    finally:
        # Возвращаем указатель в начало
        await file.seek(0)

    return True


def get_file_extension(content_type: str) -> Optional[str]:
    """
    Получить расширение файла по MIME-типу.

    Args:
        content_type: MIME-тип

    Returns:
        Optional[str]: Расширение файла или None
    """
    mime_to_ext = {
        'image/jpeg': 'jpg',
        'image/jpg': 'jpg',
        'image/png': 'png',
    }

    return mime_to_ext.get(content_type)


async def get_image_dimensions(file: UploadFile) -> tuple[int, int]:
    """
    Получить размеры изображения.

    Args:
        file: Загруженный файл

    Returns:
        tuple[int, int]: (ширина, высота)

    Raises:
        HTTPException: Если не удалось определить размеры
    """
    try:
        from PIL import Image
        import io

        content = await file.read()
        await file.seek(0)

        image = Image.open(io.BytesIO(content))
        width, height = image.size

        return width, height

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Failed to read image dimensions: {str(e)}"
        )
