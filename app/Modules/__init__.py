from flask import Blueprint

from app.Modules.Images.image_module import ImageModule
from .base_module import Module

module_bp = Blueprint("/", __name__)