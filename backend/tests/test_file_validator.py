"""
Unit тесты для модуля валидации файлов

Тестируемый модуль:
- app/services/file_validator.py — валидация изображений
"""

import pytest
import io
from unittest.mock import Mock
from fastapi import UploadFile

from app.services.file_validator import (
    validate_image_file,
    get_file_extension,
    get_image_dimensions,
)


class TestValidateImageFile:
    """Тесты валидации файлов изображений"""

    def test_valid_jpeg_file(self):
        """Тест валидации корректного JPEG файла"""
        # JPEG magic bytes (FF D8 FF)
        jpeg_content = b'\xff\xd8\xff\xe0\x00\x10JFIF\x00\x01\x01'
        file = UploadFile(
            filename="test.jpg",
            file=io.BytesIO(jpeg_content)
        )
        file.content_type = "image/jpeg"
        file.size = len(jpeg_content)

        result = validate_image_file(file)

        assert result is True

    def test_valid_png_file(self):
        """Тест валидации корректного PNG файла"""
        # PNG magic bytes (89 50 4E 47 0D 0A 1A 0A)
        png_content = b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR'
        file = UploadFile(
            filename="test.png",
            file=io.BytesIO(png_content)
        )
        file.content_type = "image/png"
        file.size = len(png_content)

        result = validate_image_file(file)

        assert result is True

    def test_invalid_mime_type(self):
        """Тест с неподдерживаемым MIME-типом"""
        content = b'some content'
        file = UploadFile(
            filename="test.gif",
            file=io.BytesIO(content)
        )
        file.content_type = "image/gif"
        file.size = len(content)

        with pytest.raises(ValueError, match="Unsupported file type"):
            validate_image_file(file)

    def test_file_too_large(self):
        """Тест с файлом больше 5MB"""
        content = b'x' * (6 * 1024 * 1024)  # 6 MB
        file = UploadFile(
            filename="test.jpg",
            file=io.BytesIO(content)
        )
        file.content_type = "image/jpeg"
        file.size = len(content)

        with pytest.raises(ValueError, match="File size exceeds 5MB"):
            validate_image_file(file)

    def test_invalid_magic_bytes_jpeg(self):
        """Тест с неправильными magic bytes для JPEG"""
        # Неправильные magic bytes, но правильный MIME-тип
        content = b'fake jpeg content'
        file = UploadFile(
            filename="test.jpg",
            file=io.BytesIO(content)
        )
        file.content_type = "image/jpeg"
        file.size = len(content)

        with pytest.raises(ValueError, match="Invalid file signature"):
            validate_image_file(file)

    def test_invalid_magic_bytes_png(self):
        """Тест с неправильными magic bytes для PNG"""
        content = b'fake png content'
        file = UploadFile(
            filename="test.png",
            file=io.BytesIO(content)
        )
        file.content_type = "image/png"
        file.size = len(content)

        with pytest.raises(ValueError, match="Invalid file signature"):
            validate_image_file(file)

    def test_mime_type_mismatch(self):
        """Тест когда MIME-тип не соответствует расширению"""
        # PNG magic bytes, но JPEG MIME-тип
        png_content = b'\x89PNG\r\n\x1a\n'
        file = UploadFile(
            filename="test.jpg",
            file=io.BytesIO(png_content)
        )
        file.content_type = "image/jpeg"
        file.size = len(png_content)

        # Должна быть ошибка, так как magic bytes не соответствуют MIME-типу
        with pytest.raises(ValueError):
            validate_image_file(file)


class TestGetFileExtension:
    """Тесты получения расширения файла"""

    def test_get_extension_from_filename(self):
        """Получение расширения из имени файла"""
        result = get_file_extension("test.jpg", "image/jpeg")

        assert result == ".jpg"

    def test_get_extension_from_mime_type(self):
        """Получение расширения из MIME-типа"""
        result = get_file_extension("test", "image/png")

        assert result == ".png"

    def test_get_extension_uppercase(self):
        """Расширение в верхнем регистре"""
        result = get_file_extension("TEST.JPEG", "image/jpeg")

        assert result == ".jpeg"

    def test_get_extension_no_extension(self):
        """Имя файла без расширения"""
        result = get_file_extension("test", "image/jpeg")

        assert result == ".jpg"


class TestGetImageDimensions:
    """Тесты получения размеров изображения"""

    @pytest.mark.skip(reason="Требует создание реального изображения с PIL")
    def test_get_dimensions_valid_image(self):
        """Получение размеров валидного изображения"""
        # TODO: Создать реальное изображение с Pillow
        pass

    @pytest.mark.skip(reason="Требует создание реального изображения с PIL")
    def test_get_dimensions_invalid_image(self):
        """Попытка получить размеры невалидного изображения"""
        # TODO: Проверить обработку ошибки
        pass
