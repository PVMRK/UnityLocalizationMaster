import json
import logging
import os
import sys
import urllib.request
import xml.etree.ElementTree as ET
from tkinter import filedialog, messagebox, simpledialog
import tkinter as tk
from tkinter import ttk
from xml.dom import minidom

# Prevent automatic proxy detection that may break translation requests on some PCs
urllib.request.getproxies = lambda: {}

try:
    from deep_translator import GoogleTranslator
except Exception:
    GoogleTranslator = None


APP_ID = "UnityLocalizationMaster"
DEFAULT_XML_LANGUAGES = ["en", "ru"]
UI_LANGUAGES = ["ru", "en", "de", "es", "fr"]
UI_LANGUAGE_NAMES = {
    "ru": "Русский",
    "en": "English",
    "de": "Deutsch",
    "es": "Español",
    "fr": "Français",
}

UI_TEXTS = {
    "en": {
        "app_title": "Unity Localization Master",
        "header_title": "Localization XML Editor",
        "header_subtitle": "Create, edit and translate Unity-style XML localization files.",
        "menu_file": "File",
        "menu_new": "Create XML...",
        "menu_open": "Open XML...",
        "menu_save": "Save XML",
        "menu_save_as": "Save XML As...",
        "menu_exit": "Exit",
        "menu_edit": "Edit",
        "menu_new_entry": "New entry",
        "menu_delete_entry": "Delete selected entry",
        "menu_clear_form": "Clear form",
        "menu_tools": "Tools",
        "menu_add_language": "Add XML language",
        "menu_auto_translate": "Auto-translate current entry",
        "menu_batch_language": "Add language and translate all entries",
        "menu_help": "Help",
        "menu_about": "About",
        "menu_ui_language": "Program language",
        "toolbar_open": "Open XML",
        "toolbar_create": "Create XML",
        "toolbar_save": "Save XML",
        "toolbar_add_language": "Add language",
        "toolbar_batch": "Translate entire file",
        "left_panel_title": "Entries",
        "search": "Search",
        "search_placeholder": "Search by key or text",
        "refresh": "Refresh",
        "new_entry": "New",
        "delete_entry": "Delete",
        "entry_id": "Entry key (ID)",
        "source_language": "Source language for translation",
        "translations": "Translations",
        "editor_title_new": "New entry",
        "editor_title_edit": "Editing: {key}",
        "save_entry": "Save entry",
        "clear_form": "Clear form",
        "auto_translate": "Auto-translate current entry",
        "batch_translate": "Add language and translate all entries",
        "status_ready": "Ready",
        "status_no_file": "No XML file selected",
        "status_file_loaded": "Loaded: {path}",
        "status_file_saved": "Saved: {path}",
        "status_entry_saved": "Entry saved: {key}",
        "status_entry_deleted": "Entry deleted: {key}",
        "status_language_added": "XML language added: {lang}",
        "status_search_results": "Found: {count}",
        "status_translation_done": "Automatic translation completed",
        "status_batch_done": "Batch translation completed: {lang}",
        "table_id": "ID",
        "table_preview": "English preview",
        "warning": "Warning",
        "error": "Error",
        "info": "Information",
        "confirm": "Confirmation",
        "about_title": "About",
        "about_text": "Unity Localization Master\n\nProduction-style desktop editor for XML localization files.\nFeatures:\n• XML entry browser\n• Interface localization into 5 languages\n• Automatic translation via Google Translator\n• Batch language generation\n• Ready for EXE packaging with PyInstaller",
        "prompt_new_file": "Create a new localization XML file?",
        "prompt_unsaved_switch": "The current form has unsaved changes. Save the entry before continuing?",
        "prompt_unsaved_exit": "The current form has unsaved changes. Exit anyway?",
        "prompt_delete_entry": "Delete entry '{key}'?",
        "prompt_overwrite_entry": "Entry '{key}' already exists. Overwrite it?",
        "prompt_replace_language": "Language '{lang}' already exists in the XML. Re-translate all entries for this language?",
        "prompt_language_code": "Enter a language code (for example: de, fr, es, it, pt-BR):",
        "prompt_language_code_all": "Enter a language code for batch translation (for example: ja, ko, tr, pt-BR):",
        "msg_open_first": "Please open or create an XML file first.",
        "msg_invalid_xml": "The selected XML file could not be read.\n\n{error}",
        "msg_key_required": "Please enter an entry key (ID).",
        "msg_entry_saved": "Entry '{key}' has been saved.",
        "msg_entry_deleted": "Entry '{key}' has been deleted.",
        "msg_nothing_selected": "Please select an entry first.",
        "msg_language_exists": "This XML language already exists.",
        "msg_language_added": "Language '{lang}' has been added to the editor.",
        "msg_no_translator": "Translation is unavailable.\nInstall dependency: pip install deep-translator",
        "msg_missing_source": "Source text is empty.",
        "msg_missing_source_lang": "Source language field is not available.",
        "msg_no_entries": "There are no entries in the XML file.",
        "msg_batch_finished": "Language '{lang}' processed.\nTranslated: {ok}\nErrors/Skipped: {failed}\nTotal entries: {total}",
        "msg_file_created": "A new XML file has been created.",
        "msg_file_saved": "XML file has been saved.",
        "msg_save_before_xml": "Save the current entry before saving the XML?",
        "msg_search_empty": "Type text to filter the entry list.",
        "msg_same_ui_language": "The program language is already selected.",
        "progress_title": "Translation in progress",
        "progress_batch_label": "Translating {total} entries into '{lang}'...",
        "progress_current_label": "Translating current entry...",
        "xml_language_list": "XML languages",
        "current_file": "Current file",
        "translator_status_on": "Translator: available",
        "translator_status_off": "Translator: unavailable",
        "field_text": "Text ({lang})",
        "footer_hint": "Tip: double-click an entry in the list to edit it quickly.",
        "language_program": "Program language",
    },
    "ru": {
        "app_title": "Unity Localization Master",
        "header_title": "Редактор XML-локализации",
        "header_subtitle": "Создание, редактирование и перевод XML-файлов локализации в стиле Unity.",
        "menu_file": "Файл",
        "menu_new": "Создать XML...",
        "menu_open": "Открыть XML...",
        "menu_save": "Сохранить XML",
        "menu_save_as": "Сохранить XML как...",
        "menu_exit": "Выход",
        "menu_edit": "Правка",
        "menu_new_entry": "Новая запись",
        "menu_delete_entry": "Удалить выбранную запись",
        "menu_clear_form": "Очистить форму",
        "menu_tools": "Инструменты",
        "menu_add_language": "Добавить язык XML",
        "menu_auto_translate": "Автоперевод текущей записи",
        "menu_batch_language": "Добавить язык и перевести все записи",
        "menu_help": "Справка",
        "menu_about": "О программе",
        "menu_ui_language": "Язык программы",
        "toolbar_open": "Открыть XML",
        "toolbar_create": "Создать XML",
        "toolbar_save": "Сохранить XML",
        "toolbar_add_language": "Добавить язык",
        "toolbar_batch": "Перевести весь файл",
        "left_panel_title": "Записи",
        "search": "Поиск",
        "search_placeholder": "Поиск по ключу или тексту",
        "refresh": "Обновить",
        "new_entry": "Новая",
        "delete_entry": "Удалить",
        "entry_id": "Ключ записи (ID)",
        "source_language": "Исходный язык для перевода",
        "translations": "Переводы",
        "editor_title_new": "Новая запись",
        "editor_title_edit": "Редактирование: {key}",
        "save_entry": "Сохранить запись",
        "clear_form": "Очистить форму",
        "auto_translate": "Автоперевод текущей записи",
        "batch_translate": "Добавить язык и перевести все записи",
        "status_ready": "Готово",
        "status_no_file": "XML-файл не выбран",
        "status_file_loaded": "Загружено: {path}",
        "status_file_saved": "Сохранено: {path}",
        "status_entry_saved": "Запись сохранена: {key}",
        "status_entry_deleted": "Запись удалена: {key}",
        "status_language_added": "Язык XML добавлен: {lang}",
        "status_search_results": "Найдено: {count}",
        "status_translation_done": "Автоперевод завершён",
        "status_batch_done": "Пакетный перевод завершён: {lang}",
        "table_id": "ID",
        "table_preview": "Предпросмотр EN",
        "warning": "Внимание",
        "error": "Ошибка",
        "info": "Информация",
        "confirm": "Подтверждение",
        "about_title": "О программе",
        "about_text": "Unity Localization Master\n\nДесктопный редактор XML-локализаций с оформлением под production.\nФункции:\n• список и поиск записей\n• локализация интерфейса на 5 языков\n• автоматический перевод через Google Translator\n• пакетное добавление языков\n• готовность к сборке в EXE через PyInstaller",
        "prompt_new_file": "Создать новый XML-файл локализации?",
        "prompt_unsaved_switch": "В текущей форме есть несохранённые изменения. Сохранить запись перед продолжением?",
        "prompt_unsaved_exit": "В текущей форме есть несохранённые изменения. Всё равно выйти?",
        "prompt_delete_entry": "Удалить запись '{key}'?",
        "prompt_overwrite_entry": "Запись '{key}' уже существует. Перезаписать её?",
        "prompt_replace_language": "Язык '{lang}' уже существует в XML. Перевести все записи для него заново?",
        "prompt_language_code": "Введите код языка (например: de, fr, es, it, pt-BR):",
        "prompt_language_code_all": "Введите код языка для пакетного перевода (например: ja, ko, tr, pt-BR):",
        "msg_open_first": "Сначала откройте или создайте XML-файл.",
        "msg_invalid_xml": "Не удалось прочитать выбранный XML-файл.\n\n{error}",
        "msg_key_required": "Введите ключ записи (ID).",
        "msg_entry_saved": "Запись '{key}' сохранена.",
        "msg_entry_deleted": "Запись '{key}' удалена.",
        "msg_nothing_selected": "Сначала выберите запись.",
        "msg_language_exists": "Этот язык XML уже существует.",
        "msg_language_added": "Язык '{lang}' добавлен в редактор.",
        "msg_no_translator": "Перевод недоступен.\nУстановите зависимость: pip install deep-translator",
        "msg_missing_source": "Исходный текст пуст.",
        "msg_missing_source_lang": "Поле исходного языка недоступно.",
        "msg_no_entries": "В XML-файле нет записей.",
        "msg_batch_finished": "Язык '{lang}' обработан.\nПереведено: {ok}\nОшибок/пропущено: {failed}\nВсего записей: {total}",
        "msg_file_created": "Новый XML-файл создан.",
        "msg_file_saved": "XML-файл сохранён.",
        "msg_save_before_xml": "Сохранить текущую запись перед сохранением XML?",
        "msg_search_empty": "Введите текст, чтобы отфильтровать список записей.",
        "msg_same_ui_language": "Этот язык программы уже выбран.",
        "progress_title": "Идёт перевод",
        "progress_batch_label": "Перевод {total} записей на '{lang}'...",
        "progress_current_label": "Перевод текущей записи...",
        "xml_language_list": "Языки XML",
        "current_file": "Текущий файл",
        "translator_status_on": "Переводчик: доступен",
        "translator_status_off": "Переводчик: недоступен",
        "field_text": "Текст ({lang})",
        "footer_hint": "Совет: дважды кликните по записи в списке, чтобы быстро открыть её для редактирования.",
        "language_program": "Язык программы",
    },
    "de": {
        "app_title": "Unity Localization Master",
        "header_title": "XML-Lokalisierungseditor",
        "header_subtitle": "Unity-ähnliche XML-Lokalisierungsdateien erstellen, bearbeiten und übersetzen.",
        "menu_file": "Datei",
        "menu_new": "XML erstellen...",
        "menu_open": "XML öffnen...",
        "menu_save": "XML speichern",
        "menu_save_as": "XML speichern unter...",
        "menu_exit": "Beenden",
        "menu_edit": "Bearbeiten",
        "menu_new_entry": "Neuer Eintrag",
        "menu_delete_entry": "Ausgewählten Eintrag löschen",
        "menu_clear_form": "Formular leeren",
        "menu_tools": "Werkzeuge",
        "menu_add_language": "XML-Sprache hinzufügen",
        "menu_auto_translate": "Aktuellen Eintrag automatisch übersetzen",
        "menu_batch_language": "Sprache hinzufügen und alle Einträge übersetzen",
        "menu_help": "Hilfe",
        "menu_about": "Info",
        "menu_ui_language": "Programmsprache",
        "toolbar_open": "XML öffnen",
        "toolbar_create": "XML erstellen",
        "toolbar_save": "XML speichern",
        "toolbar_add_language": "Sprache hinzufügen",
        "toolbar_batch": "Gesamte Datei übersetzen",
        "left_panel_title": "Einträge",
        "search": "Suche",
        "search_placeholder": "Nach Schlüssel oder Text suchen",
        "refresh": "Aktualisieren",
        "new_entry": "Neu",
        "delete_entry": "Löschen",
        "entry_id": "Eintrags-ID",
        "source_language": "Quellsprache für Übersetzung",
        "translations": "Übersetzungen",
        "editor_title_new": "Neuer Eintrag",
        "editor_title_edit": "Bearbeiten: {key}",
        "save_entry": "Eintrag speichern",
        "clear_form": "Formular leeren",
        "auto_translate": "Aktuellen Eintrag automatisch übersetzen",
        "batch_translate": "Sprache hinzufügen und alle Einträge übersetzen",
        "status_ready": "Bereit",
        "status_no_file": "Keine XML-Datei ausgewählt",
        "status_file_loaded": "Geladen: {path}",
        "status_file_saved": "Gespeichert: {path}",
        "status_entry_saved": "Eintrag gespeichert: {key}",
        "status_entry_deleted": "Eintrag gelöscht: {key}",
        "status_language_added": "XML-Sprache hinzugefügt: {lang}",
        "status_search_results": "Gefunden: {count}",
        "status_translation_done": "Automatische Übersetzung abgeschlossen",
        "status_batch_done": "Stapelübersetzung abgeschlossen: {lang}",
        "table_id": "ID",
        "table_preview": "EN-Vorschau",
        "warning": "Warnung",
        "error": "Fehler",
        "info": "Information",
        "confirm": "Bestätigung",
        "about_title": "Info",
        "about_text": "Unity Localization Master\n\nDesktop-Editor im Production-Stil für XML-Lokalisierungsdateien.\nFunktionen:\n• Eintragsliste und Suche\n• Oberfläche in 5 Sprachen\n• Automatische Übersetzung über Google Translator\n• Stapelweises Hinzufügen von Sprachen\n• Bereit für EXE-Build mit PyInstaller",
        "prompt_new_file": "Neue XML-Lokalisierungsdatei erstellen?",
        "prompt_unsaved_switch": "Im aktuellen Formular gibt es ungespeicherte Änderungen. Eintrag vor dem Fortfahren speichern?",
        "prompt_unsaved_exit": "Im aktuellen Formular gibt es ungespeicherte Änderungen. Trotzdem beenden?",
        "prompt_delete_entry": "Eintrag '{key}' löschen?",
        "prompt_overwrite_entry": "Eintrag '{key}' existiert bereits. Überschreiben?",
        "prompt_replace_language": "Sprache '{lang}' existiert bereits in der XML-Datei. Alle Einträge erneut für diese Sprache übersetzen?",
        "prompt_language_code": "Sprachcode eingeben (z. B. de, fr, es, it, pt-BR):",
        "prompt_language_code_all": "Sprachcode für Stapelübersetzung eingeben (z. B. ja, ko, tr, pt-BR):",
        "msg_open_first": "Bitte zuerst eine XML-Datei öffnen oder erstellen.",
        "msg_invalid_xml": "Die ausgewählte XML-Datei konnte nicht gelesen werden.\n\n{error}",
        "msg_key_required": "Bitte eine Eintrags-ID eingeben.",
        "msg_entry_saved": "Eintrag '{key}' wurde gespeichert.",
        "msg_entry_deleted": "Eintrag '{key}' wurde gelöscht.",
        "msg_nothing_selected": "Bitte zuerst einen Eintrag auswählen.",
        "msg_language_exists": "Diese XML-Sprache existiert bereits.",
        "msg_language_added": "Sprache '{lang}' wurde zum Editor hinzugefügt.",
        "msg_no_translator": "Übersetzung ist nicht verfügbar.\nAbhängigkeit installieren: pip install deep-translator",
        "msg_missing_source": "Quelltext ist leer.",
        "msg_missing_source_lang": "Das Feld der Quellsprache ist nicht verfügbar.",
        "msg_no_entries": "Die XML-Datei enthält keine Einträge.",
        "msg_batch_finished": "Sprache '{lang}' verarbeitet.\nÜbersetzt: {ok}\nFehler/Übersprungen: {failed}\nGesamteinträge: {total}",
        "msg_file_created": "Neue XML-Datei wurde erstellt.",
        "msg_file_saved": "XML-Datei wurde gespeichert.",
        "msg_save_before_xml": "Aktuellen Eintrag vor dem Speichern der XML-Datei speichern?",
        "msg_search_empty": "Text eingeben, um die Eintragsliste zu filtern.",
        "msg_same_ui_language": "Diese Programmsprache ist bereits ausgewählt.",
        "progress_title": "Übersetzung läuft",
        "progress_batch_label": "Übersetze {total} Einträge nach '{lang}'...",
        "progress_current_label": "Aktuellen Eintrag übersetzen...",
        "xml_language_list": "XML-Sprachen",
        "current_file": "Aktuelle Datei",
        "translator_status_on": "Übersetzer: verfügbar",
        "translator_status_off": "Übersetzer: nicht verfügbar",
        "field_text": "Text ({lang})",
        "footer_hint": "Tipp: Doppelklicken Sie auf einen Eintrag in der Liste, um ihn schnell zu bearbeiten.",
        "language_program": "Programmsprache",
    },
    "es": {
        "app_title": "Unity Localization Master",
        "header_title": "Editor de localización XML",
        "header_subtitle": "Crea, edita y traduce archivos XML de localización estilo Unity.",
        "menu_file": "Archivo",
        "menu_new": "Crear XML...",
        "menu_open": "Abrir XML...",
        "menu_save": "Guardar XML",
        "menu_save_as": "Guardar XML como...",
        "menu_exit": "Salir",
        "menu_edit": "Editar",
        "menu_new_entry": "Nueva entrada",
        "menu_delete_entry": "Eliminar entrada seleccionada",
        "menu_clear_form": "Limpiar formulario",
        "menu_tools": "Herramientas",
        "menu_add_language": "Agregar idioma XML",
        "menu_auto_translate": "Traducir automáticamente la entrada actual",
        "menu_batch_language": "Agregar idioma y traducir todas las entradas",
        "menu_help": "Ayuda",
        "menu_about": "Acerca de",
        "menu_ui_language": "Idioma del programa",
        "toolbar_open": "Abrir XML",
        "toolbar_create": "Crear XML",
        "toolbar_save": "Guardar XML",
        "toolbar_add_language": "Agregar idioma",
        "toolbar_batch": "Traducir todo el archivo",
        "left_panel_title": "Entradas",
        "search": "Buscar",
        "search_placeholder": "Buscar por clave o texto",
        "refresh": "Actualizar",
        "new_entry": "Nueva",
        "delete_entry": "Eliminar",
        "entry_id": "Clave de entrada (ID)",
        "source_language": "Idioma de origen para traducción",
        "translations": "Traducciones",
        "editor_title_new": "Nueva entrada",
        "editor_title_edit": "Editando: {key}",
        "save_entry": "Guardar entrada",
        "clear_form": "Limpiar formulario",
        "auto_translate": "Traducir automáticamente la entrada actual",
        "batch_translate": "Agregar idioma y traducir todas las entradas",
        "status_ready": "Listo",
        "status_no_file": "No se ha seleccionado un archivo XML",
        "status_file_loaded": "Cargado: {path}",
        "status_file_saved": "Guardado: {path}",
        "status_entry_saved": "Entrada guardada: {key}",
        "status_entry_deleted": "Entrada eliminada: {key}",
        "status_language_added": "Idioma XML agregado: {lang}",
        "status_search_results": "Encontrados: {count}",
        "status_translation_done": "Traducción automática completada",
        "status_batch_done": "Traducción masiva completada: {lang}",
        "table_id": "ID",
        "table_preview": "Vista previa EN",
        "warning": "Advertencia",
        "error": "Error",
        "info": "Información",
        "confirm": "Confirmación",
        "about_title": "Acerca de",
        "about_text": "Unity Localization Master\n\nEditor de escritorio con estilo production para archivos XML de localización.\nFunciones:\n• lista y búsqueda de entradas\n• interfaz traducida a 5 idiomas\n• traducción automática mediante Google Translator\n• generación masiva de idiomas\n• listo para compilar en EXE con PyInstaller",
        "prompt_new_file": "¿Crear un nuevo archivo XML de localización?",
        "prompt_unsaved_switch": "Hay cambios no guardados en el formulario actual. ¿Guardar la entrada antes de continuar?",
        "prompt_unsaved_exit": "Hay cambios no guardados en el formulario actual. ¿Salir de todos modos?",
        "prompt_delete_entry": "¿Eliminar la entrada '{key}'?",
        "prompt_overwrite_entry": "La entrada '{key}' ya existe. ¿Sobrescribirla?",
        "prompt_replace_language": "El idioma '{lang}' ya existe en el XML. ¿Volver a traducir todas las entradas para este idioma?",
        "prompt_language_code": "Introduce un código de idioma (por ejemplo: de, fr, es, it, pt-BR):",
        "prompt_language_code_all": "Introduce un código de idioma para traducción masiva (por ejemplo: ja, ko, tr, pt-BR):",
        "msg_open_first": "Primero abre o crea un archivo XML.",
        "msg_invalid_xml": "No se pudo leer el archivo XML seleccionado.\n\n{error}",
        "msg_key_required": "Introduce una clave de entrada (ID).",
        "msg_entry_saved": "La entrada '{key}' ha sido guardada.",
        "msg_entry_deleted": "La entrada '{key}' ha sido eliminada.",
        "msg_nothing_selected": "Primero selecciona una entrada.",
        "msg_language_exists": "Este idioma XML ya existe.",
        "msg_language_added": "El idioma '{lang}' ha sido agregado al editor.",
        "msg_no_translator": "La traducción no está disponible.\nInstala la dependencia: pip install deep-translator",
        "msg_missing_source": "El texto de origen está vacío.",
        "msg_missing_source_lang": "El campo del idioma de origen no está disponible.",
        "msg_no_entries": "No hay entradas en el archivo XML.",
        "msg_batch_finished": "Idioma '{lang}' procesado.\nTraducidos: {ok}\nErrores/Omitidos: {failed}\nEntradas totales: {total}",
        "msg_file_created": "Se ha creado un nuevo archivo XML.",
        "msg_file_saved": "El archivo XML ha sido guardado.",
        "msg_save_before_xml": "¿Guardar la entrada actual antes de guardar el XML?",
        "msg_search_empty": "Escribe texto para filtrar la lista de entradas.",
        "msg_same_ui_language": "Ese idioma del programa ya está seleccionado.",
        "progress_title": "Traducción en progreso",
        "progress_batch_label": "Traduciendo {total} entradas a '{lang}'...",
        "progress_current_label": "Traduciendo la entrada actual...",
        "xml_language_list": "Idiomas XML",
        "current_file": "Archivo actual",
        "translator_status_on": "Traductor: disponible",
        "translator_status_off": "Traductor: no disponible",
        "field_text": "Texto ({lang})",
        "footer_hint": "Consejo: haz doble clic en una entrada de la lista para editarla rápidamente.",
        "language_program": "Idioma del programa",
    },
    "fr": {
        "app_title": "Unity Localization Master",
        "header_title": "Éditeur de localisation XML",
        "header_subtitle": "Créez, modifiez et traduisez des fichiers XML de localisation au style Unity.",
        "menu_file": "Fichier",
        "menu_new": "Créer un XML...",
        "menu_open": "Ouvrir un XML...",
        "menu_save": "Enregistrer le XML",
        "menu_save_as": "Enregistrer le XML sous...",
        "menu_exit": "Quitter",
        "menu_edit": "Édition",
        "menu_new_entry": "Nouvelle entrée",
        "menu_delete_entry": "Supprimer l'entrée sélectionnée",
        "menu_clear_form": "Effacer le formulaire",
        "menu_tools": "Outils",
        "menu_add_language": "Ajouter une langue XML",
        "menu_auto_translate": "Traduire automatiquement l'entrée actuelle",
        "menu_batch_language": "Ajouter une langue et traduire toutes les entrées",
        "menu_help": "Aide",
        "menu_about": "À propos",
        "menu_ui_language": "Langue du programme",
        "toolbar_open": "Ouvrir XML",
        "toolbar_create": "Créer XML",
        "toolbar_save": "Enregistrer XML",
        "toolbar_add_language": "Ajouter une langue",
        "toolbar_batch": "Traduire tout le fichier",
        "left_panel_title": "Entrées",
        "search": "Recherche",
        "search_placeholder": "Rechercher par clé ou texte",
        "refresh": "Actualiser",
        "new_entry": "Nouvelle",
        "delete_entry": "Supprimer",
        "entry_id": "Clé de l'entrée (ID)",
        "source_language": "Langue source pour la traduction",
        "translations": "Traductions",
        "editor_title_new": "Nouvelle entrée",
        "editor_title_edit": "Modification : {key}",
        "save_entry": "Enregistrer l'entrée",
        "clear_form": "Effacer le formulaire",
        "auto_translate": "Traduire automatiquement l'entrée actuelle",
        "batch_translate": "Ajouter une langue et traduire toutes les entrées",
        "status_ready": "Prêt",
        "status_no_file": "Aucun fichier XML sélectionné",
        "status_file_loaded": "Chargé : {path}",
        "status_file_saved": "Enregistré : {path}",
        "status_entry_saved": "Entrée enregistrée : {key}",
        "status_entry_deleted": "Entrée supprimée : {key}",
        "status_language_added": "Langue XML ajoutée : {lang}",
        "status_search_results": "Trouvés : {count}",
        "status_translation_done": "Traduction automatique terminée",
        "status_batch_done": "Traduction par lot terminée : {lang}",
        "table_id": "ID",
        "table_preview": "Aperçu EN",
        "warning": "Avertissement",
        "error": "Erreur",
        "info": "Information",
        "confirm": "Confirmation",
        "about_title": "À propos",
        "about_text": "Unity Localization Master\n\nÉditeur de bureau de style production pour les fichiers XML de localisation.\nFonctionnalités :\n• liste et recherche d'entrées\n• interface localisée en 5 langues\n• traduction automatique via Google Translator\n• ajout massif de langues\n• prêt pour une compilation EXE avec PyInstaller",
        "prompt_new_file": "Créer un nouveau fichier XML de localisation ?",
        "prompt_unsaved_switch": "Le formulaire actuel contient des modifications non enregistrées. Enregistrer l'entrée avant de continuer ?",
        "prompt_unsaved_exit": "Le formulaire actuel contient des modifications non enregistrées. Quitter quand même ?",
        "prompt_delete_entry": "Supprimer l'entrée '{key}' ?",
        "prompt_overwrite_entry": "L'entrée '{key}' existe déjà. L'écraser ?",
        "prompt_replace_language": "La langue '{lang}' existe déjà dans le XML. Retraduire toutes les entrées pour cette langue ?",
        "prompt_language_code": "Entrez un code de langue (par ex. : de, fr, es, it, pt-BR) :",
        "prompt_language_code_all": "Entrez un code de langue pour la traduction par lot (par ex. : ja, ko, tr, pt-BR) :",
        "msg_open_first": "Veuillez d'abord ouvrir ou créer un fichier XML.",
        "msg_invalid_xml": "Impossible de lire le fichier XML sélectionné.\n\n{error}",
        "msg_key_required": "Veuillez saisir une clé d'entrée (ID).",
        "msg_entry_saved": "L'entrée '{key}' a été enregistrée.",
        "msg_entry_deleted": "L'entrée '{key}' a été supprimée.",
        "msg_nothing_selected": "Veuillez d'abord sélectionner une entrée.",
        "msg_language_exists": "Cette langue XML existe déjà.",
        "msg_language_added": "La langue '{lang}' a été ajoutée à l'éditeur.",
        "msg_no_translator": "La traduction n'est pas disponible.\nInstallez la dépendance : pip install deep-translator",
        "msg_missing_source": "Le texte source est vide.",
        "msg_missing_source_lang": "Le champ de langue source n'est pas disponible.",
        "msg_no_entries": "Le fichier XML ne contient aucune entrée.",
        "msg_batch_finished": "Langue '{lang}' traitée.\nTraduites : {ok}\nErreurs/Ignorées : {failed}\nNombre total d'entrées : {total}",
        "msg_file_created": "Un nouveau fichier XML a été créé.",
        "msg_file_saved": "Le fichier XML a été enregistré.",
        "msg_save_before_xml": "Enregistrer l'entrée actuelle avant d'enregistrer le XML ?",
        "msg_search_empty": "Saisissez du texte pour filtrer la liste des entrées.",
        "msg_same_ui_language": "Cette langue du programme est déjà sélectionnée.",
        "progress_title": "Traduction en cours",
        "progress_batch_label": "Traduction de {total} entrées vers '{lang}'...",
        "progress_current_label": "Traduction de l'entrée actuelle...",
        "xml_language_list": "Langues XML",
        "current_file": "Fichier actuel",
        "translator_status_on": "Traducteur : disponible",
        "translator_status_off": "Traducteur : indisponible",
        "field_text": "Texte ({lang})",
        "footer_hint": "Astuce : double-cliquez sur une entrée dans la liste pour l'ouvrir rapidement en modification.",
        "language_program": "Langue du programme",
    },
}

EXTRA_UI_TEXTS = {
    "en": {
        "menu_tutorial": "Quick tutorial",
        "tutorial_window_title": "Quick tutorial",
        "tutorial_step_counter": "Step {current} of {total}",
        "tutorial_prev": "Previous",
        "tutorial_next": "Next",
        "tutorial_close": "Close",
        "tutorial_focus": "Show",
        "tutorial_intro_body": "This short tour shows the main workflow: open or create XML, pick an entry, edit translations and save the result.",
        "tooltip_open": "Open an existing XML localization file.",
        "tooltip_create": "Create a new empty XML localization file.",
        "tooltip_save_xml": "Write all current entries back to the XML file on disk.",
        "tooltip_add_language": "Add a new language column to the current XML file.",
        "tooltip_batch": "Generate a new language for the whole file using automatic translation.",
        "tooltip_search": "Filter the entry list by key or translated text.",
        "tooltip_entries": "This list contains all localization keys. Double-click an item to edit it.",
        "tooltip_entry_id": "Each localization entry needs a unique key used by the game or app.",
        "tooltip_source_language": "Choose which language will be used as the source for automatic translation.",
        "tooltip_save_entry": "Save the current entry to the XML data.",
        "tooltip_clear_form": "Clear the editor and start a new entry.",
        "tooltip_auto_translate": "Fill the other language fields from the selected source language.",
        "tooltip_translations": "Edit the texts for every XML language here.",
        "tooltip_language_switch": "Switch the program interface language instantly.",
        "tooltip_current_file": "Shows the XML file currently opened in the editor.",
    },
    "ru": {
        "menu_tutorial": "Быстрое обучение",
        "tutorial_window_title": "Быстрое обучение",
        "tutorial_step_counter": "Шаг {current} из {total}",
        "tutorial_prev": "Назад",
        "tutorial_next": "Далее",
        "tutorial_close": "Закрыть",
        "tutorial_focus": "Показать",
        "tutorial_intro_body": "Этот короткий тур показывает основной сценарий работы: открыть или создать XML, выбрать запись, отредактировать переводы и сохранить результат.",
        "tooltip_open": "Открыть существующий XML-файл локализации.",
        "tooltip_create": "Создать новый пустой XML-файл локализации.",
        "tooltip_save_xml": "Записать все текущие записи обратно в XML-файл на диске.",
        "tooltip_add_language": "Добавить новый языковой столбец в текущий XML-файл.",
        "tooltip_batch": "Сгенерировать новый язык для всего файла с помощью автоперевода.",
        "tooltip_search": "Фильтровать список записей по ключу или переведённому тексту.",
        "tooltip_entries": "Здесь находятся все ключи локализации. Дважды кликните по записи, чтобы отредактировать её.",
        "tooltip_entry_id": "Каждой записи локализации нужен уникальный ключ, который использует игра или приложение.",
        "tooltip_source_language": "Выберите язык, который будет исходным для автоматического перевода.",
        "tooltip_save_entry": "Сохранить текущую запись в XML-данные.",
        "tooltip_clear_form": "Очистить редактор и начать новую запись.",
        "tooltip_auto_translate": "Заполнить остальные языки на основе выбранного исходного языка.",
        "tooltip_translations": "Редактируйте здесь тексты для всех языков XML.",
        "tooltip_language_switch": "Мгновенно переключить язык интерфейса программы.",
        "tooltip_current_file": "Показывает XML-файл, который сейчас открыт в редакторе.",
    },
    "de": {
        "menu_tutorial": "Kurzanleitung",
        "tutorial_window_title": "Kurzanleitung",
        "tutorial_step_counter": "Schritt {current} von {total}",
        "tutorial_prev": "Zurück",
        "tutorial_next": "Weiter",
        "tutorial_close": "Schließen",
        "tutorial_focus": "Anzeigen",
        "tutorial_intro_body": "Diese kurze Tour zeigt den Hauptablauf: XML öffnen oder erstellen, einen Eintrag wählen, Übersetzungen bearbeiten und das Ergebnis speichern.",
        "tooltip_open": "Eine vorhandene XML-Lokalisierungsdatei öffnen.",
        "tooltip_create": "Eine neue leere XML-Lokalisierungsdatei erstellen.",
        "tooltip_save_xml": "Alle aktuellen Einträge zurück in die XML-Datei auf dem Datenträger schreiben.",
        "tooltip_add_language": "Eine neue Sprachspalte zur aktuellen XML-Datei hinzufügen.",
        "tooltip_batch": "Eine neue Sprache für die gesamte Datei per automatischer Übersetzung erzeugen.",
        "tooltip_search": "Die Eintragsliste nach Schlüssel oder übersetztem Text filtern.",
        "tooltip_entries": "Diese Liste enthält alle Lokalisierungsschlüssel. Doppelklicken Sie auf einen Eintrag, um ihn zu bearbeiten.",
        "tooltip_entry_id": "Jeder Lokalisierungseintrag benötigt einen eindeutigen Schlüssel, der vom Spiel oder der App verwendet wird.",
        "tooltip_source_language": "Wählen Sie die Sprache, die als Quelle für die automatische Übersetzung verwendet wird.",
        "tooltip_save_entry": "Den aktuellen Eintrag in den XML-Daten speichern.",
        "tooltip_clear_form": "Den Editor leeren und einen neuen Eintrag beginnen.",
        "tooltip_auto_translate": "Die anderen Sprachfelder aus der gewählten Quellsprache füllen.",
        "tooltip_translations": "Bearbeiten Sie hier die Texte für alle XML-Sprachen.",
        "tooltip_language_switch": "Die Programmsprache sofort umschalten.",
        "tooltip_current_file": "Zeigt die XML-Datei an, die aktuell im Editor geöffnet ist.",
    },
    "es": {
        "menu_tutorial": "Tutorial rápido",
        "tutorial_window_title": "Tutorial rápido",
        "tutorial_step_counter": "Paso {current} de {total}",
        "tutorial_prev": "Anterior",
        "tutorial_next": "Siguiente",
        "tutorial_close": "Cerrar",
        "tutorial_focus": "Mostrar",
        "tutorial_intro_body": "Este recorrido corto muestra el flujo principal: abrir o crear XML, elegir una entrada, editar traducciones y guardar el resultado.",
        "tooltip_open": "Abrir un archivo XML de localización existente.",
        "tooltip_create": "Crear un archivo XML de localización vacío.",
        "tooltip_save_xml": "Escribir todas las entradas actuales de nuevo en el archivo XML del disco.",
        "tooltip_add_language": "Agregar una nueva columna de idioma al archivo XML actual.",
        "tooltip_batch": "Generar un nuevo idioma para todo el archivo usando traducción automática.",
        "tooltip_search": "Filtrar la lista de entradas por clave o texto traducido.",
        "tooltip_entries": "Esta lista contiene todas las claves de localización. Haz doble clic en un elemento para editarlo.",
        "tooltip_entry_id": "Cada entrada de localización necesita una clave única usada por el juego o la aplicación.",
        "tooltip_source_language": "Elige el idioma que se usará como fuente para la traducción automática.",
        "tooltip_save_entry": "Guardar la entrada actual en los datos XML.",
        "tooltip_clear_form": "Limpiar el editor y empezar una nueva entrada.",
        "tooltip_auto_translate": "Rellenar los demás idiomas desde el idioma de origen seleccionado.",
        "tooltip_translations": "Edita aquí los textos para todos los idiomas XML.",
        "tooltip_language_switch": "Cambiar al instante el idioma de la interfaz del programa.",
        "tooltip_current_file": "Muestra el archivo XML que está abierto actualmente en el editor.",
    },
    "fr": {
        "menu_tutorial": "Tutoriel rapide",
        "tutorial_window_title": "Tutoriel rapide",
        "tutorial_step_counter": "Étape {current} sur {total}",
        "tutorial_prev": "Précédent",
        "tutorial_next": "Suivant",
        "tutorial_close": "Fermer",
        "tutorial_focus": "Afficher",
        "tutorial_intro_body": "Cette courte visite montre le flux principal : ouvrir ou créer un XML, choisir une entrée, modifier les traductions et enregistrer le résultat.",
        "tooltip_open": "Ouvrir un fichier XML de localisation existant.",
        "tooltip_create": "Créer un nouveau fichier XML de localisation vide.",
        "tooltip_save_xml": "Écrire toutes les entrées actuelles dans le fichier XML sur le disque.",
        "tooltip_add_language": "Ajouter une nouvelle colonne de langue au fichier XML actuel.",
        "tooltip_batch": "Générer une nouvelle langue pour tout le fichier à l'aide de la traduction automatique.",
        "tooltip_search": "Filtrer la liste des entrées par clé ou par texte traduit.",
        "tooltip_entries": "Cette liste contient toutes les clés de localisation. Double-cliquez sur un élément pour le modifier.",
        "tooltip_entry_id": "Chaque entrée de localisation a besoin d'une clé unique utilisée par le jeu ou l'application.",
        "tooltip_source_language": "Choisissez la langue qui servira de source pour la traduction automatique.",
        "tooltip_save_entry": "Enregistrer l'entrée actuelle dans les données XML.",
        "tooltip_clear_form": "Effacer l'éditeur et commencer une nouvelle entrée.",
        "tooltip_auto_translate": "Remplir les autres langues à partir de la langue source sélectionnée.",
        "tooltip_translations": "Modifiez ici les textes pour toutes les langues XML.",
        "tooltip_language_switch": "Changer instantanément la langue de l'interface du programme.",
        "tooltip_current_file": "Affiche le fichier XML actuellement ouvert dans l'éditeur.",
    },
}

for lang_code, localized_values in EXTRA_UI_TEXTS.items():
    UI_TEXTS.setdefault(lang_code, {}).update(localized_values)


def ensure_app_dir():
    if os.name == "nt":
        base = os.getenv("APPDATA") or os.path.expanduser("~")
    else:
        base = os.path.join(os.path.expanduser("~"), ".config")
    app_dir = os.path.join(base, APP_ID)
    os.makedirs(app_dir, exist_ok=True)
    return app_dir


APP_DIR = ensure_app_dir()
SETTINGS_PATH = os.path.join(APP_DIR, "settings.json")
LOG_PATH = os.path.join(APP_DIR, "app.log")


def setup_logging():
    logging.basicConfig(
        filename=LOG_PATH,
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(message)s",
    )


class ToolTip:
    def __init__(self, widget, text="", delay=350):
        self.widget = widget
        self.text = text
        self.delay = delay
        self.tip_window = None
        self.after_id = None
        self.widget.bind("<Enter>", self.schedule, add="+")
        self.widget.bind("<Leave>", self.hide, add="+")
        self.widget.bind("<ButtonPress>", self.hide, add="+")

    def set_text(self, text):
        self.text = text

    def schedule(self, _event=None):
        self.unschedule()
        self.after_id = self.widget.after(self.delay, self.show)

    def unschedule(self):
        if self.after_id:
            self.widget.after_cancel(self.after_id)
            self.after_id = None

    def show(self):
        if self.tip_window or not self.text:
            return
        x = self.widget.winfo_rootx() + 16
        y = self.widget.winfo_rooty() + self.widget.winfo_height() + 10

        self.tip_window = tw = tk.Toplevel(self.widget)
        tw.wm_overrideredirect(True)
        try:
            tw.attributes("-topmost", True)
        except Exception:
            pass
        tw.configure(bg="#111827")

        label = tk.Label(
            tw,
            text=self.text,
            justify="left",
            bg="#111827",
            fg="#F9FAFB",
            padx=10,
            pady=8,
            font=("Segoe UI", 9),
            wraplength=320,
        )
        label.pack()
        tw.wm_geometry(f"+{x}+{y}")

    def hide(self, _event=None):
        self.unschedule()
        if self.tip_window is not None:
            self.tip_window.destroy()
            self.tip_window = None


class LocalizationEditorApp:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.minsize(1180, 760)
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)

        self.settings = self.load_settings()
        self.ui_language = self.settings.get("ui_language", "en")
        if self.ui_language not in UI_LANGUAGES:
            self.ui_language = "en"

        self.xml_path = ""
        self.entries = []
        self.languages = []
        self.filtered_entry_ids = []
        self.current_entry_id = None
        self.form_dirty = False
        self.widgets_ready = False
        self.text_inputs = {}
        self.translation_frames = {}
        self.tooltip_objects = {}
        self.tutorial_window = None
        self.tutorial_step_index = 0
        self.tutorial_steps_cache = []

        self.style = ttk.Style()
        self.configure_styles()

        self.translator_available = GoogleTranslator is not None
        if self.translator_available:
            try:
                GoogleTranslator(source="en", target="de").translate("test")
            except Exception as exc:
                logging.warning("Translator self-test failed: %s", exc)
                self.translator_available = False

        self.search_var = tk.StringVar()
        self.entry_id_var = tk.StringVar()
        self.source_lang_var = tk.StringVar()
        self.ui_lang_var = tk.StringVar(value=self.ui_language)
        self.status_var = tk.StringVar()
        self.current_file_var = tk.StringVar()
        self.languages_var = tk.StringVar()
        self.translator_var = tk.StringVar()
        self.editor_title_var = tk.StringVar()

        self.build_ui()
        self.restore_window_geometry()
        self.apply_ui_language(initial=True)
        self.mark_clean()
        self.root.after(700, self.maybe_show_startup_tutorial)

    def tr(self, key: str, **kwargs) -> str:
        text = UI_TEXTS.get(self.ui_language, UI_TEXTS["en"]).get(key)
        if text is None:
            text = UI_TEXTS["en"].get(key, key)
        if kwargs:
            try:
                return text.format(**kwargs)
            except Exception:
                return text
        return text

    def load_settings(self):
        if not os.path.exists(SETTINGS_PATH):
            return {}
        try:
            with open(SETTINGS_PATH, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception as exc:
            logging.warning("Failed to load settings: %s", exc)
            return {}

    def save_settings(self):
        data = {
            "ui_language": self.ui_language,
            "geometry": self.root.geometry(),
            "last_xml_path": self.xml_path,
            "tutorial_seen": self.settings.get("tutorial_seen", False),
        }
        try:
            with open(SETTINGS_PATH, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
        except Exception as exc:
            logging.warning("Failed to save settings: %s", exc)

    def restore_window_geometry(self):
        geometry = self.settings.get("geometry")
        if geometry:
            try:
                self.root.geometry(geometry)
            except Exception:
                self.root.geometry("1280x820")
        else:
            self.root.geometry("1280x820")

    def configure_styles(self):
        self.style.theme_use("clam")
        colors = {
            "bg": "#F4F7FB",
            "surface": "#FFFFFF",
            "surface_alt": "#EEF3F9",
            "border": "#D7E0EA",
            "text": "#1F2937",
            "muted": "#6B7280",
            "accent": "#2563EB",
            "accent_hover": "#1D4ED8",
            "success": "#16A34A",
            "success_hover": "#15803D",
            "danger": "#DC2626",
            "danger_hover": "#B91C1C",
        }
        self.colors = colors

        self.root.configure(bg=colors["bg"])
        self.style.configure("TFrame", background=colors["bg"])
        self.style.configure("Surface.TFrame", background=colors["surface"])
        self.style.configure("Toolbar.TFrame", background=colors["bg"])
        self.style.configure("Header.TFrame", background=colors["bg"])
        self.style.configure(
            "Card.TLabelframe",
            background=colors["surface"],
            foreground=colors["text"],
            borderwidth=1,
            relief="solid",
        )
        self.style.configure(
            "Card.TLabelframe.Label",
            background=colors["surface"],
            foreground=colors["text"],
            font=("Segoe UI", 11, "bold"),
        )
        self.style.configure("TLabel", background=colors["bg"], foreground=colors["text"], font=("Segoe UI", 10))
        self.style.configure("Title.TLabel", background=colors["bg"], foreground=colors["text"], font=("Segoe UI", 20, "bold"))
        self.style.configure("Subtitle.TLabel", background=colors["bg"], foreground=colors["muted"], font=("Segoe UI", 10))
        self.style.configure("Section.TLabel", background=colors["surface"], foreground=colors["text"], font=("Segoe UI", 10, "bold"))
        self.style.configure("Hint.TLabel", background=colors["bg"], foreground=colors["muted"], font=("Segoe UI", 9))
        self.style.configure("Info.TLabel", background=colors["surface"], foreground=colors["muted"], font=("Segoe UI", 9))
        self.style.configure(
            "TButton",
            font=("Segoe UI", 10),
            padding=(14, 8),
            borderwidth=0,
        )
        self.style.map("TButton", background=[("active", colors["surface_alt"])])
        self.style.configure(
            "Accent.TButton",
            background=colors["accent"],
            foreground="#FFFFFF",
            padding=(16, 9),
            borderwidth=0,
        )
        self.style.map(
            "Accent.TButton",
            background=[("active", colors["accent_hover"]), ("pressed", colors["accent_hover"])],
            foreground=[("disabled", "#D1D5DB")],
        )
        self.style.configure(
            "Success.TButton",
            background=colors["success"],
            foreground="#FFFFFF",
            padding=(16, 9),
            borderwidth=0,
        )
        self.style.map(
            "Success.TButton",
            background=[("active", colors["success_hover"]), ("pressed", colors["success_hover"])],
        )
        self.style.configure(
            "Danger.TButton",
            background=colors["danger"],
            foreground="#FFFFFF",
            padding=(16, 9),
            borderwidth=0,
        )
        self.style.map(
            "Danger.TButton",
            background=[("active", colors["danger_hover"]), ("pressed", colors["danger_hover"])],
        )
        self.style.configure(
            "TEntry",
            fieldbackground=colors["surface"],
            bordercolor=colors["border"],
            lightcolor=colors["border"],
            darkcolor=colors["border"],
            padding=8,
        )
        self.style.configure(
            "TCombobox",
            fieldbackground=colors["surface"],
            background=colors["surface"],
            bordercolor=colors["border"],
            arrowsize=14,
            padding=6,
        )
        self.style.configure(
            "Treeview",
            background=colors["surface"],
            fieldbackground=colors["surface"],
            foreground=colors["text"],
            bordercolor=colors["border"],
            rowheight=30,
            font=("Segoe UI", 10),
        )
        self.style.configure(
            "Treeview.Heading",
            background=colors["surface_alt"],
            foreground=colors["text"],
            font=("Segoe UI", 10, "bold"),
            relief="flat",
        )
        self.style.map("Treeview", background=[("selected", colors["accent"])], foreground=[("selected", "#FFFFFF")])
        self.style.configure("TSeparator", background=colors["border"])
        self.style.configure("TProgressbar", troughcolor=colors["surface_alt"], bordercolor=colors["border"], background=colors["accent"], lightcolor=colors["accent"], darkcolor=colors["accent"])

    def build_ui(self):
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(2, weight=1)

        self.menu_bar = tk.Menu(self.root)
        self.root.config(menu=self.menu_bar)

        self.file_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.edit_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.tools_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.language_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.help_menu = tk.Menu(self.menu_bar, tearoff=0)

        self.build_menus()

        header = ttk.Frame(self.root, style="Header.TFrame")
        header.grid(row=0, column=0, sticky="ew", padx=18, pady=(18, 8))
        header.columnconfigure(0, weight=1)
        header.columnconfigure(1, weight=0)

        title_box = ttk.Frame(header, style="Header.TFrame")
        title_box.grid(row=0, column=0, sticky="w")
        self.header_title_label = ttk.Label(title_box, style="Title.TLabel")
        self.header_title_label.pack(anchor="w")
        self.header_subtitle_label = ttk.Label(title_box, style="Subtitle.TLabel")
        self.header_subtitle_label.pack(anchor="w", pady=(2, 0))

        lang_box = ttk.Frame(header, style="Header.TFrame")
        lang_box.grid(row=0, column=1, sticky="e")
        self.program_language_label = ttk.Label(lang_box)
        self.program_language_label.pack(anchor="e")
        self.ui_lang_combo = ttk.Combobox(
            lang_box,
            state="readonly",
            width=18,
            values=[UI_LANGUAGE_NAMES[code] for code in UI_LANGUAGES],
        )
        self.ui_lang_combo.pack(anchor="e", pady=(6, 0))
        self.ui_lang_combo.current(UI_LANGUAGES.index(self.ui_language))
        self.ui_lang_combo.bind("<<ComboboxSelected>>", self.on_ui_language_changed)

        toolbar = ttk.Frame(self.root, style="Toolbar.TFrame")
        toolbar.grid(row=1, column=0, sticky="ew", padx=18, pady=(0, 10))
        for col in range(6):
            toolbar.columnconfigure(col, weight=0)
        toolbar.columnconfigure(6, weight=1)

        self.open_button = ttk.Button(toolbar, command=self.open_xml_file)
        self.open_button.grid(row=0, column=0, padx=(0, 8), pady=4)
        self.create_button = ttk.Button(toolbar, command=self.create_xml_file)
        self.create_button.grid(row=0, column=1, padx=(0, 8), pady=4)
        self.save_xml_button = ttk.Button(toolbar, style="Success.TButton", command=self.save_xml_file)
        self.save_xml_button.grid(row=0, column=2, padx=(0, 8), pady=4)
        self.add_language_button = ttk.Button(toolbar, command=self.add_new_language)
        self.add_language_button.grid(row=0, column=3, padx=(0, 8), pady=4)
        self.batch_button = ttk.Button(toolbar, style="Accent.TButton", command=self.add_language_and_translate_all)
        self.batch_button.grid(row=0, column=4, padx=(0, 8), pady=4)

        info_box = ttk.Frame(toolbar, style="Toolbar.TFrame")
        info_box.grid(row=0, column=6, sticky="e")
        self.current_file_label = ttk.Label(info_box, style="Hint.TLabel")
        self.current_file_label.pack(anchor="e")
        self.current_file_value = ttk.Label(info_box, style="Hint.TLabel", textvariable=self.current_file_var)
        self.current_file_value.pack(anchor="e")

        content = ttk.Panedwindow(self.root, orient=tk.HORIZONTAL)
        content.grid(row=2, column=0, sticky="nsew", padx=18, pady=(0, 10))

        self.left_card = ttk.LabelFrame(content, style="Card.TLabelframe")
        self.right_card = ttk.LabelFrame(content, style="Card.TLabelframe")
        content.add(self.left_card, weight=1)
        content.add(self.right_card, weight=2)

        self.build_left_panel(self.left_card)
        self.build_right_panel(self.right_card)

        footer = ttk.Frame(self.root, style="Header.TFrame")
        footer.grid(row=3, column=0, sticky="ew", padx=18, pady=(0, 18))
        footer.columnconfigure(0, weight=1)
        footer.columnconfigure(1, weight=0)

        self.footer_hint_label = ttk.Label(footer, style="Hint.TLabel")
        self.footer_hint_label.grid(row=0, column=0, sticky="w")

        status_holder = ttk.Frame(footer, style="Header.TFrame")
        status_holder.grid(row=0, column=1, sticky="e")
        self.status_label = ttk.Label(status_holder, style="Hint.TLabel", textvariable=self.status_var)
        self.status_label.pack(anchor="e")
        self.translator_label = ttk.Label(status_holder, style="Hint.TLabel", textvariable=self.translator_var)
        self.translator_label.pack(anchor="e")

        self.widgets_ready = True
        self.apply_tooltips()

    def build_menus(self):
        self.menu_bar.delete(0, "end")
        self.file_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.edit_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.tools_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.language_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.help_menu = tk.Menu(self.menu_bar, tearoff=0)

        self.file_menu.add_command(label=self.tr("menu_new"), command=self.create_xml_file)
        self.file_menu.add_command(label=self.tr("menu_open"), command=self.open_xml_file)
        self.file_menu.add_separator()
        self.file_menu.add_command(label=self.tr("menu_save"), command=self.save_xml_file)
        self.file_menu.add_command(label=self.tr("menu_save_as"), command=self.save_xml_as)
        self.file_menu.add_separator()
        self.file_menu.add_command(label=self.tr("menu_exit"), command=self.on_close)

        self.edit_menu.add_command(label=self.tr("menu_new_entry"), command=self.clear_form)
        self.edit_menu.add_command(label=self.tr("menu_delete_entry"), command=self.delete_selected_entry)
        self.edit_menu.add_separator()
        self.edit_menu.add_command(label=self.tr("menu_clear_form"), command=self.clear_form)

        self.tools_menu.add_command(label=self.tr("menu_add_language"), command=self.add_new_language)
        self.tools_menu.add_command(label=self.tr("menu_auto_translate"), command=self.auto_translate_current)
        self.tools_menu.add_command(label=self.tr("menu_batch_language"), command=self.add_language_and_translate_all)

        for code in UI_LANGUAGES:
            self.language_menu.add_command(
                label=UI_LANGUAGE_NAMES[code],
                command=lambda c=code: self.set_ui_language(c),
            )

        self.help_menu.add_command(label=self.tr("menu_tutorial"), command=self.open_tutorial)
        self.help_menu.add_separator()
        self.help_menu.add_command(label=self.tr("menu_about"), command=self.show_about)

        self.menu_bar.add_cascade(label=self.tr("menu_file"), menu=self.file_menu)
        self.menu_bar.add_cascade(label=self.tr("menu_edit"), menu=self.edit_menu)
        self.menu_bar.add_cascade(label=self.tr("menu_tools"), menu=self.tools_menu)
        self.menu_bar.add_cascade(label=self.tr("menu_ui_language"), menu=self.language_menu)
        self.menu_bar.add_cascade(label=self.tr("menu_help"), menu=self.help_menu)

    def build_left_panel(self, parent):
        parent.columnconfigure(0, weight=1)
        parent.rowconfigure(2, weight=1)

        top = ttk.Frame(parent, style="Surface.TFrame")
        top.grid(row=0, column=0, sticky="ew", padx=14, pady=(12, 10))
        top.columnconfigure(1, weight=1)

        self.search_label = ttk.Label(top, style="Section.TLabel")
        self.search_label.grid(row=0, column=0, sticky="w", padx=(0, 10))

        self.search_entry = ttk.Entry(top, textvariable=self.search_var)
        self.search_entry.grid(row=0, column=1, sticky="ew", padx=(0, 8))
        self.search_var.trace_add("write", lambda *_: self.filter_entries())

        self.refresh_button = ttk.Button(top, command=self.filter_entries)
        self.refresh_button.grid(row=0, column=2, sticky="e")

        actions = ttk.Frame(parent, style="Surface.TFrame")
        actions.grid(row=1, column=0, sticky="ew", padx=14, pady=(0, 10))
        actions.columnconfigure(0, weight=1)
        actions.columnconfigure(1, weight=1)

        self.new_entry_button = ttk.Button(actions, command=self.clear_form)
        self.new_entry_button.grid(row=0, column=0, sticky="ew", padx=(0, 6))
        self.delete_entry_button = ttk.Button(actions, style="Danger.TButton", command=self.delete_selected_entry)
        self.delete_entry_button.grid(row=0, column=1, sticky="ew", padx=(6, 0))

        table_holder = ttk.Frame(parent, style="Surface.TFrame")
        table_holder.grid(row=2, column=0, sticky="nsew", padx=14, pady=(0, 10))
        table_holder.columnconfigure(0, weight=1)
        table_holder.rowconfigure(0, weight=1)

        self.entry_tree = ttk.Treeview(table_holder, columns=("id", "preview"), show="headings", selectmode="browse")
        self.entry_tree.grid(row=0, column=0, sticky="nsew")
        self.entry_tree.bind("<<TreeviewSelect>>", self.on_tree_select)
        self.entry_tree.bind("<Double-1>", self.on_tree_double_click)

        tree_scroll = ttk.Scrollbar(table_holder, orient="vertical", command=self.entry_tree.yview)
        tree_scroll.grid(row=0, column=1, sticky="ns")
        self.entry_tree.configure(yscrollcommand=tree_scroll.set)

        info_holder = ttk.Frame(parent, style="Surface.TFrame")
        info_holder.grid(row=3, column=0, sticky="ew", padx=14, pady=(0, 12))
        info_holder.columnconfigure(0, weight=1)

        self.xml_languages_label = ttk.Label(info_holder, style="Section.TLabel")
        self.xml_languages_label.grid(row=0, column=0, sticky="w")
        self.xml_languages_value = ttk.Label(info_holder, style="Info.TLabel", textvariable=self.languages_var, wraplength=320, justify="left")
        self.xml_languages_value.grid(row=1, column=0, sticky="ew", pady=(4, 8))

    def build_right_panel(self, parent):
        parent.columnconfigure(0, weight=1)
        parent.rowconfigure(4, weight=1)

        top = ttk.Frame(parent, style="Surface.TFrame")
        top.grid(row=0, column=0, sticky="ew", padx=16, pady=(12, 10))
        top.columnconfigure(1, weight=1)
        top.columnconfigure(3, weight=0)

        self.editor_title_label = ttk.Label(top, style="Section.TLabel", textvariable=self.editor_title_var)
        self.editor_title_label.grid(row=0, column=0, columnspan=4, sticky="w", pady=(0, 12))

        self.entry_id_label = ttk.Label(top)
        self.entry_id_label.grid(row=1, column=0, sticky="w", padx=(0, 10))
        self.entry_id_entry = ttk.Entry(top, textvariable=self.entry_id_var)
        self.entry_id_entry.grid(row=1, column=1, sticky="ew", padx=(0, 12))
        self.entry_id_entry.bind("<KeyRelease>", self.mark_dirty_event)

        self.source_language_label = ttk.Label(top)
        self.source_language_label.grid(row=1, column=2, sticky="w", padx=(0, 10))
        self.source_language_combo = ttk.Combobox(top, state="readonly", textvariable=self.source_lang_var, width=10)
        self.source_language_combo.grid(row=1, column=3, sticky="ew")

        action_bar = ttk.Frame(parent, style="Surface.TFrame")
        action_bar.grid(row=1, column=0, sticky="ew", padx=16, pady=(0, 10))
        for col in range(4):
            action_bar.columnconfigure(col, weight=1)

        self.save_entry_button = ttk.Button(action_bar, style="Success.TButton", command=self.save_entry)
        self.save_entry_button.grid(row=0, column=0, sticky="ew", padx=(0, 6))
        self.clear_button = ttk.Button(action_bar, command=self.clear_form)
        self.clear_button.grid(row=0, column=1, sticky="ew", padx=6)
        self.auto_translate_button = ttk.Button(action_bar, command=self.auto_translate_current)
        self.auto_translate_button.grid(row=0, column=2, sticky="ew", padx=6)
        self.batch_translate_button = ttk.Button(action_bar, style="Accent.TButton", command=self.add_language_and_translate_all)
        self.batch_translate_button.grid(row=0, column=3, sticky="ew", padx=(6, 0))

        self.translations_label = ttk.Label(parent, style="Section.TLabel")
        self.translations_label.grid(row=2, column=0, sticky="w", padx=16, pady=(0, 6))

        card = ttk.Frame(parent, style="Surface.TFrame")
        card.grid(row=4, column=0, sticky="nsew", padx=16, pady=(0, 14))
        card.columnconfigure(0, weight=1)
        card.rowconfigure(0, weight=1)

        self.translation_canvas = tk.Canvas(
            card,
            bg=self.colors["surface"],
            bd=0,
            highlightthickness=0,
            relief="flat",
        )
        self.translation_canvas.grid(row=0, column=0, sticky="nsew")
        translation_scroll = ttk.Scrollbar(card, orient="vertical", command=self.translation_canvas.yview)
        translation_scroll.grid(row=0, column=1, sticky="ns")
        self.translation_canvas.configure(yscrollcommand=translation_scroll.set)

        self.translation_container = ttk.Frame(card, style="Surface.TFrame")
        self.translation_container.bind(
            "<Configure>",
            lambda e: self.translation_canvas.configure(scrollregion=self.translation_canvas.bbox("all")),
        )
        self.translation_window = self.translation_canvas.create_window((0, 0), window=self.translation_container, anchor="nw")
        self.translation_canvas.bind("<Configure>", self.on_translation_canvas_resize)
        self.translation_canvas.bind_all("<MouseWheel>", self.on_mouse_wheel)

    def on_translation_canvas_resize(self, event):
        self.translation_canvas.itemconfig(self.translation_window, width=event.width)

    def on_mouse_wheel(self, event):
        if self.translation_canvas.winfo_exists():
            self.translation_canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

    def attach_tooltip(self, widget, text):
        if widget is None or not text:
            return
        tooltip = self.tooltip_objects.get(widget)
        if tooltip is None:
            self.tooltip_objects[widget] = ToolTip(widget, text)
        else:
            tooltip.set_text(text)

    def apply_tooltips(self):
        if not self.widgets_ready:
            return
        tooltip_map = [
            (self.ui_lang_combo, self.tr("tooltip_language_switch")),
            (self.open_button, self.tr("tooltip_open")),
            (self.create_button, self.tr("tooltip_create")),
            (self.save_xml_button, self.tr("tooltip_save_xml")),
            (self.add_language_button, self.tr("tooltip_add_language")),
            (self.batch_button, self.tr("tooltip_batch")),
            (self.current_file_value, self.tr("tooltip_current_file")),
            (self.search_entry, self.tr("tooltip_search")),
            (self.entry_tree, self.tr("tooltip_entries")),
            (self.entry_id_entry, self.tr("tooltip_entry_id")),
            (self.source_language_combo, self.tr("tooltip_source_language")),
            (self.save_entry_button, self.tr("tooltip_save_entry")),
            (self.clear_button, self.tr("tooltip_clear_form")),
            (self.auto_translate_button, self.tr("tooltip_auto_translate")),
        ]
        for widget, text in tooltip_map:
            self.attach_tooltip(widget, text)

        for widget in self.text_inputs.values():
            self.attach_tooltip(widget, self.tr("tooltip_translations"))

    def get_tutorial_steps(self):
        translation_target = next(iter(self.text_inputs.values()), self.translations_label)
        return [
            {
                "widget": self.header_title_label,
                "title": self.tr("header_title"),
                "body": self.tr("tutorial_intro_body"),
            },
            {
                "widget": self.open_button,
                "title": f"{self.tr('toolbar_open')} / {self.tr('toolbar_create')}",
                "body": f"• {self.tr('tooltip_open')}\n• {self.tr('tooltip_create')}\n• {self.tr('tooltip_current_file')}",
            },
            {
                "widget": self.entry_tree,
                "title": self.tr("left_panel_title"),
                "body": f"• {self.tr('tooltip_search')}\n• {self.tr('tooltip_entries')}",
            },
            {
                "widget": self.entry_id_entry,
                "title": self.tr("entry_id"),
                "body": self.tr("tooltip_entry_id"),
            },
            {
                "widget": self.source_language_combo,
                "title": self.tr("source_language"),
                "body": f"• {self.tr('tooltip_source_language')}\n• {self.tr('tooltip_auto_translate')}",
            },
            {
                "widget": translation_target,
                "title": self.tr("translations"),
                "body": self.tr("tooltip_translations"),
            },
            {
                "widget": self.save_entry_button,
                "title": f"{self.tr('save_entry')} / {self.tr('toolbar_save')}",
                "body": f"• {self.tr('tooltip_save_entry')}\n• {self.tr('tooltip_save_xml')}",
            },
            {
                "widget": self.batch_button,
                "title": self.tr("batch_translate"),
                "body": f"• {self.tr('tooltip_add_language')}\n• {self.tr('tooltip_batch')}",
            },
        ]

    def maybe_show_startup_tutorial(self):
        if not self.settings.get("tutorial_seen", False):
            self.open_tutorial(0)

    def open_tutorial(self, step_index=0):
        self.settings["tutorial_seen"] = True
        self.save_settings()
        self.tutorial_steps_cache = self.get_tutorial_steps()
        if not self.tutorial_steps_cache:
            return

        if self.tutorial_window is None or not self.tutorial_window.winfo_exists():
            self.tutorial_window = tk.Toplevel(self.root)
            self.tutorial_window.title(self.tr("tutorial_window_title"))
            self.tutorial_window.geometry("430x280")
            self.tutorial_window.minsize(430, 280)
            self.tutorial_window.transient(self.root)
            self.tutorial_window.configure(bg=self.colors["bg"])
            self.tutorial_window.protocol("WM_DELETE_WINDOW", self.close_tutorial)

            holder = ttk.Frame(self.tutorial_window, style="Header.TFrame")
            holder.pack(fill="both", expand=True, padx=16, pady=16)
            holder.columnconfigure(0, weight=1)

            self.tutorial_progress_var = tk.StringVar()
            self.tutorial_title_var = tk.StringVar()
            self.tutorial_body_var = tk.StringVar()

            self.tutorial_progress_label = ttk.Label(holder, style="Hint.TLabel", textvariable=self.tutorial_progress_var)
            self.tutorial_progress_label.grid(row=0, column=0, sticky="w")

            self.tutorial_title_label = ttk.Label(holder, style="Title.TLabel", textvariable=self.tutorial_title_var)
            self.tutorial_title_label.grid(row=1, column=0, sticky="w", pady=(6, 10))

            self.tutorial_body_label = ttk.Label(
                holder,
                style="Section.TLabel",
                textvariable=self.tutorial_body_var,
                wraplength=380,
                justify="left",
            )
            self.tutorial_body_label.grid(row=2, column=0, sticky="nsew")

            button_bar = ttk.Frame(holder, style="Header.TFrame")
            button_bar.grid(row=3, column=0, sticky="ew", pady=(18, 0))
            button_bar.columnconfigure(0, weight=1)
            button_bar.columnconfigure(1, weight=0)
            button_bar.columnconfigure(2, weight=0)
            button_bar.columnconfigure(3, weight=0)

            self.tutorial_prev_button = ttk.Button(button_bar, command=self.tutorial_prev_step)
            self.tutorial_prev_button.grid(row=0, column=1, padx=(0, 8))
            self.tutorial_focus_button = ttk.Button(button_bar, command=self.tutorial_focus_current)
            self.tutorial_focus_button.grid(row=0, column=2, padx=(0, 8))
            self.tutorial_next_button = ttk.Button(button_bar, style="Accent.TButton", command=self.tutorial_next_step)
            self.tutorial_next_button.grid(row=0, column=3, padx=(0, 8))
            self.tutorial_close_button = ttk.Button(button_bar, command=self.close_tutorial)
            self.tutorial_close_button.grid(row=0, column=4)
        else:
            self.tutorial_window.deiconify()
            self.tutorial_window.lift()

        self.tutorial_step_index = max(0, min(step_index, len(self.tutorial_steps_cache) - 1))
        self.show_tutorial_step()

    def show_tutorial_step(self):
        if self.tutorial_window is None or not self.tutorial_window.winfo_exists():
            return
        self.tutorial_steps_cache = self.get_tutorial_steps()
        if not self.tutorial_steps_cache:
            return

        total = len(self.tutorial_steps_cache)
        self.tutorial_step_index = max(0, min(self.tutorial_step_index, total - 1))
        step = self.tutorial_steps_cache[self.tutorial_step_index]

        self.tutorial_window.title(self.tr("tutorial_window_title"))
        self.tutorial_progress_var.set(self.tr("tutorial_step_counter", current=self.tutorial_step_index + 1, total=total))
        self.tutorial_title_var.set(step["title"])
        self.tutorial_body_var.set(step["body"])
        self.tutorial_prev_button.configure(text=self.tr("tutorial_prev"), state=("disabled" if self.tutorial_step_index == 0 else "normal"))
        self.tutorial_focus_button.configure(text=self.tr("tutorial_focus"))
        self.tutorial_next_button.configure(text=self.tr("tutorial_next"), state=("disabled" if self.tutorial_step_index >= total - 1 else "normal"))
        self.tutorial_close_button.configure(text=self.tr("tutorial_close"))
        self.position_tutorial_window(step.get("widget"))

    def tutorial_prev_step(self):
        if self.tutorial_step_index > 0:
            self.tutorial_step_index -= 1
            self.show_tutorial_step()

    def tutorial_next_step(self):
        if self.tutorial_steps_cache and self.tutorial_step_index < len(self.tutorial_steps_cache) - 1:
            self.tutorial_step_index += 1
            self.show_tutorial_step()

    def tutorial_focus_current(self):
        if not self.tutorial_steps_cache:
            return
        step = self.tutorial_steps_cache[self.tutorial_step_index]
        widget = step.get("widget")
        if widget is None or not widget.winfo_exists():
            return
        try:
            widget.focus_set()
        except Exception:
            pass
        if isinstance(widget, tk.Text):
            widget.see("1.0")
        elif isinstance(widget, ttk.Treeview):
            children = widget.get_children()
            if children:
                widget.see(children[0])
        self.position_tutorial_window(widget)

    def position_tutorial_window(self, widget):
        if self.tutorial_window is None or not self.tutorial_window.winfo_exists():
            return
        self.root.update_idletasks()
        self.tutorial_window.update_idletasks()

        width = max(self.tutorial_window.winfo_width(), 430)
        height = max(self.tutorial_window.winfo_height(), 280)

        if widget is not None and widget.winfo_exists():
            x = widget.winfo_rootx() + widget.winfo_width() + 18
            y = max(24, widget.winfo_rooty() - 8)
            screen_w = self.root.winfo_screenwidth()
            screen_h = self.root.winfo_screenheight()
            if x + width > screen_w - 30:
                x = max(20, widget.winfo_rootx() - width - 18)
            if y + height > screen_h - 50:
                y = max(20, screen_h - height - 60)
        else:
            x = self.root.winfo_rootx() + 80
            y = self.root.winfo_rooty() + 80

        self.tutorial_window.geometry(f"{width}x{height}+{x}+{y}")

    def close_tutorial(self):
        if self.tutorial_window is not None and self.tutorial_window.winfo_exists():
            self.tutorial_window.destroy()
        self.tutorial_window = None

    def mark_dirty_event(self, _event=None):
        self.mark_dirty()

    def mark_dirty(self):
        self.form_dirty = True
        self.update_title()

    def mark_clean(self):
        self.form_dirty = False
        self.update_title()

    def update_title(self):
        file_name = os.path.basename(self.xml_path) if self.xml_path else self.tr("status_no_file")
        dirty = " *" if self.form_dirty else ""
        self.root.title(f"{self.tr('app_title')} — {file_name}{dirty}")

    def apply_ui_language(self, initial=False):
        current_form_data = self.collect_form_translations() if self.text_inputs else {}
        current_key_value = self.entry_id_var.get() if hasattr(self, "entry_id_var") else ""
        was_dirty = self.form_dirty

        self.build_menus()
        if not self.widgets_ready:
            return

        self.header_title_label.configure(text=self.tr("header_title"))
        self.header_subtitle_label.configure(text=self.tr("header_subtitle"))
        self.program_language_label.configure(text=self.tr("language_program"))

        self.open_button.configure(text=self.tr("toolbar_open"))
        self.create_button.configure(text=self.tr("toolbar_create"))
        self.save_xml_button.configure(text=self.tr("toolbar_save"))
        self.add_language_button.configure(text=self.tr("toolbar_add_language"))
        self.batch_button.configure(text=self.tr("toolbar_batch"))

        self.left_card.configure(text=self.tr("left_panel_title"))
        self.right_card.configure(text=self.tr("translations"))

        self.current_file_label.configure(text=self.tr("current_file"))
        self.search_label.configure(text=self.tr("search"))
        self.refresh_button.configure(text=self.tr("refresh"))
        self.new_entry_button.configure(text=self.tr("new_entry"))
        self.delete_entry_button.configure(text=self.tr("delete_entry"))
        self.xml_languages_label.configure(text=self.tr("xml_language_list"))

        self.entry_id_label.configure(text=self.tr("entry_id"))
        self.source_language_label.configure(text=self.tr("source_language"))
        self.save_entry_button.configure(text=self.tr("save_entry"))
        self.clear_button.configure(text=self.tr("clear_form"))
        self.auto_translate_button.configure(text=self.tr("auto_translate"))
        self.batch_translate_button.configure(text=self.tr("batch_translate"))
        self.translations_label.configure(text=self.tr("translations"))

        self.entry_tree.heading("id", text=self.tr("table_id"))
        self.entry_tree.heading("preview", text=self.tr("table_preview"))
        self.entry_tree.column("id", width=200, anchor="w")
        self.entry_tree.column("preview", width=320, anchor="w")

        self.footer_hint_label.configure(text=self.tr("footer_hint"))
        self.translator_var.set(self.tr("translator_status_on") if self.translator_available else self.tr("translator_status_off"))

        if initial and self.settings.get("last_xml_path") and os.path.exists(self.settings.get("last_xml_path")):
            try:
                self.load_xml_from_path(self.settings.get("last_xml_path"), silent=True)
            except Exception as exc:
                logging.warning("Failed to auto-open last XML: %s", exc)

        self.update_editor_title()
        if not self.status_var.get() or self.status_var.get() in [
            UI_TEXTS[lang].get("status_ready") for lang in UI_LANGUAGES
        ]:
            self.status_var.set(self.tr("status_ready"))
        self.update_current_file_label()
        self.refresh_language_panels()
        if current_key_value or any(current_form_data.values()):
            self.entry_id_var.set(current_key_value)
            for lang, text in current_form_data.items():
                widget = self.text_inputs.get(lang)
                if widget:
                    widget.delete("1.0", tk.END)
                    widget.insert("1.0", text)
            self.update_editor_title()
            if was_dirty:
                self.mark_dirty()
            else:
                self.mark_clean()
        self.apply_tooltips()
        if self.tutorial_window is not None and self.tutorial_window.winfo_exists():
            self.show_tutorial_step()
        self.filter_entries()
        self.update_title()
        self.save_settings()

    def update_editor_title(self):
        if self.current_entry_id:
            self.editor_title_var.set(self.tr("editor_title_edit", key=self.current_entry_id))
        else:
            self.editor_title_var.set(self.tr("editor_title_new"))

    def update_current_file_label(self):
        self.current_file_var.set(self.xml_path if self.xml_path else self.tr("status_no_file"))
        self.languages_var.set(", ".join(self.languages) if self.languages else "—")

    def set_status(self, key_or_text, literal=False, **kwargs):
        if literal:
            text = key_or_text
        else:
            text = self.tr(key_or_text, **kwargs)
        self.status_var.set(text)

    def on_ui_language_changed(self, _event=None):
        selected_name = self.ui_lang_combo.get()
        for code, name in UI_LANGUAGE_NAMES.items():
            if name == selected_name:
                self.set_ui_language(code)
                return

    def set_ui_language(self, code):
        if code not in UI_LANGUAGES:
            return
        if code == self.ui_language:
            self.ui_lang_combo.current(UI_LANGUAGES.index(code))
            return
        self.ui_language = code
        self.ui_lang_var.set(code)
        self.ui_lang_combo.current(UI_LANGUAGES.index(code))
        self.apply_ui_language()
        logging.info("UI language switched to %s", code)

    def ensure_file_selected(self):
        if self.xml_path:
            return True
        messagebox.showwarning(self.tr("warning"), self.tr("msg_open_first"))
        return False

    def create_xml_file(self):
        path = filedialog.asksaveasfilename(
            defaultextension=".xml",
            filetypes=[("XML files", "*.xml")],
            title=self.tr("menu_new"),
        )
        if not path:
            return

        root_xml = ET.Element("Languages")
        xml_content = self.prettify_xml(root_xml)
        with open(path, "w", encoding="utf-8") as f:
            f.write(xml_content)

        self.xml_path = path
        self.entries = []
        self.languages = DEFAULT_XML_LANGUAGES.copy()
        self.current_entry_id = None
        self.clear_form(force=True)
        self.refresh_language_panels()
        self.filter_entries()
        self.update_current_file_label()
        self.mark_clean()
        self.set_status("status_file_saved", path=path)
        messagebox.showinfo(self.tr("info"), self.tr("msg_file_created"))
        self.save_settings()
        logging.info("Created XML file: %s", path)

    def open_xml_file(self):
        path = filedialog.askopenfilename(
            filetypes=[("XML files", "*.xml")],
            title=self.tr("menu_open"),
        )
        if path:
            self.load_xml_from_path(path)

    def load_xml_from_path(self, path, silent=False):
        try:
            tree = ET.parse(path)
            root_xml = tree.getroot()
            entries = []
            languages = set()
            for entry in root_xml.findall("Entry"):
                key = entry.get("id", "").strip()
                if not key:
                    continue
                translations = {}
                for child in entry:
                    languages.add(child.tag)
                    translations[child.tag] = child.text or ""
                entries.append({"id": key, "translations": translations})

            self.xml_path = path
            self.entries = sorted(entries, key=lambda item: item["id"].lower())
            self.languages = sorted(languages) if languages else DEFAULT_XML_LANGUAGES.copy()
            if "en" in self.languages:
                self.source_lang_var.set("en")
            elif self.languages:
                self.source_lang_var.set(self.languages[0])

            self.current_entry_id = None
            self.refresh_language_panels()
            self.clear_form(force=True)
            self.filter_entries()
            self.update_current_file_label()
            self.mark_clean()
            self.set_status("status_file_loaded", path=path)
            self.save_settings()
            logging.info("Loaded XML file: %s", path)
        except Exception as exc:
            logging.exception("Failed to open XML: %s", path)
            if not silent:
                messagebox.showerror(self.tr("error"), self.tr("msg_invalid_xml", error=exc))

    def get_entry_by_id(self, key):
        for entry in self.entries:
            if entry["id"] == key:
                return entry
        return None

    def filter_entries(self):
        search_text = self.search_var.get().strip().lower()
        self.entry_tree.delete(*self.entry_tree.get_children())

        visible_entries = []
        for entry in self.entries:
            haystack = [entry["id"].lower()]
            haystack.extend((value or "").lower() for value in entry["translations"].values())
            if not search_text or any(search_text in text for text in haystack):
                visible_entries.append(entry)

        for entry in visible_entries:
            preview = (entry["translations"].get("en") or "").replace("\n", " ").strip()
            if len(preview) > 80:
                preview = preview[:77] + "..."
            self.entry_tree.insert("", "end", iid=entry["id"], values=(entry["id"], preview))

        self.filtered_entry_ids = [entry["id"] for entry in visible_entries]
        self.set_status("status_search_results", count=len(visible_entries))

    def on_tree_select(self, _event=None):
        selection = self.entry_tree.selection()
        if not selection:
            return
        key = selection[0]
        if self.current_entry_id == key:
            return
        if self.form_dirty and any(self.collect_form_translations().values()) or (self.entry_id_var.get().strip() and self.form_dirty):
            should_save = messagebox.askyesnocancel(self.tr("confirm"), self.tr("prompt_unsaved_switch"))
            if should_save is None:
                self.entry_tree.selection_remove(selection)
                if self.current_entry_id:
                    self.entry_tree.selection_set(self.current_entry_id)
                return
            if should_save:
                if not self.save_entry(show_success=False):
                    self.entry_tree.selection_remove(selection)
                    if self.current_entry_id:
                        self.entry_tree.selection_set(self.current_entry_id)
                    return
        self.load_entry_into_form(key)

    def on_tree_double_click(self, _event=None):
        selection = self.entry_tree.selection()
        if selection:
            self.load_entry_into_form(selection[0])

    def load_entry_into_form(self, key):
        entry = self.get_entry_by_id(key)
        if not entry:
            return
        self.current_entry_id = key
        self.entry_id_var.set(entry["id"])
        for lang in self.languages:
            widget = self.text_inputs.get(lang)
            if not widget:
                continue
            widget.delete("1.0", tk.END)
            widget.insert("1.0", entry["translations"].get(lang, ""))
        self.update_editor_title()
        self.mark_clean()
        self.set_status("status_ready")

    def refresh_language_panels(self):
        for child in self.translation_container.winfo_children():
            child.destroy()
        self.text_inputs.clear()
        self.translation_frames.clear()

        if not self.languages:
            self.languages = DEFAULT_XML_LANGUAGES.copy()

        for index, lang in enumerate(self.languages):
            box = ttk.LabelFrame(self.translation_container, text=self.tr("field_text", lang=lang.upper()), style="Card.TLabelframe")
            box.grid(row=index, column=0, sticky="ew", padx=0, pady=(0, 10))
            box.columnconfigure(0, weight=1)

            text = tk.Text(
                box,
                height=4,
                wrap="word",
                undo=True,
                font=("Segoe UI", 10),
                bg=self.colors["surface"],
                fg=self.colors["text"],
                insertbackground=self.colors["text"],
                relief="flat",
                bd=0,
                highlightthickness=1,
                highlightbackground=self.colors["border"],
                highlightcolor=self.colors["accent"],
                padx=10,
                pady=10,
            )
            text.grid(row=0, column=0, sticky="ew")
            text.bind("<KeyRelease>", self.mark_dirty_event)
            self.text_inputs[lang] = text
            self.translation_frames[lang] = box

        combo_values = self.languages.copy()
        self.source_language_combo.configure(values=combo_values)
        preferred = self.source_lang_var.get()
        if preferred not in combo_values:
            preferred = "en" if "en" in combo_values else (combo_values[0] if combo_values else "")
        self.source_lang_var.set(preferred)
        self.update_current_file_label()
        self.apply_tooltips()
        if self.tutorial_window is not None and self.tutorial_window.winfo_exists():
            self.show_tutorial_step()

    def collect_form_translations(self):
        data = {}
        for lang, widget in self.text_inputs.items():
            text = widget.get("1.0", tk.END).rstrip("\n")
            data[lang] = text
        return data

    def clear_form(self, force=False):
        has_any_data = bool(self.entry_id_var.get().strip()) or any(self.collect_form_translations().values())
        if not force and self.form_dirty and has_any_data:
            answer = messagebox.askyesnocancel(self.tr("confirm"), self.tr("prompt_unsaved_switch"))
            if answer is None:
                return
            if answer:
                if not self.save_entry(show_success=False):
                    return

        self.current_entry_id = None
        self.entry_id_var.set("")
        for widget in self.text_inputs.values():
            widget.delete("1.0", tk.END)
        selected = self.entry_tree.selection()
        if selected:
            self.entry_tree.selection_remove(*selected)
        self.update_editor_title()
        self.mark_clean()
        self.set_status("status_ready")

    def sort_entries(self):
        self.entries = sorted(self.entries, key=lambda item: item["id"].lower())

    def write_xml_to_path(self, path):
        root_xml = ET.Element("Languages")
        self.sort_entries()
        for entry in self.entries:
            entry_node = ET.SubElement(root_xml, "Entry", id=entry["id"])
            translations = entry.get("translations", {})
            for lang in self.languages:
                node = ET.SubElement(entry_node, lang)
                node.text = translations.get(lang, "")

        xml_content = self.prettify_xml(root_xml)
        if os.path.exists(path):
            try:
                backup_path = path + ".bak"
                with open(path, "r", encoding="utf-8") as src, open(backup_path, "w", encoding="utf-8") as dst:
                    dst.write(src.read())
            except Exception as exc:
                logging.warning("Failed to create backup for %s: %s", path, exc)

        with open(path, "w", encoding="utf-8") as f:
            f.write(xml_content)

    def prettify_xml(self, root_xml):
        raw = ET.tostring(root_xml, encoding="utf-8")
        parsed = minidom.parseString(raw)
        pretty = parsed.toprettyxml(indent="  ", encoding="utf-8")
        return b"\n".join(line for line in pretty.splitlines() if line.strip()).decode("utf-8")

    def save_entry(self, show_success=True):
        if not self.ensure_file_selected():
            return False

        key = self.entry_id_var.get().strip()
        if not key:
            messagebox.showwarning(self.tr("warning"), self.tr("msg_key_required"))
            return False

        translations = self.collect_form_translations()
        current_entry = self.get_entry_by_id(self.current_entry_id) if self.current_entry_id else None
        existing_target = self.get_entry_by_id(key)

        if existing_target and existing_target is not current_entry:
            overwrite = messagebox.askyesno(self.tr("confirm"), self.tr("prompt_overwrite_entry", key=key))
            if not overwrite:
                return False
            self.entries.remove(existing_target)

        if current_entry is not None:
            current_entry["id"] = key
            current_entry["translations"] = translations
        else:
            self.entries.append({"id": key, "translations": translations})

        self.current_entry_id = key
        self.write_xml_to_path(self.xml_path)
        self.sort_entries()
        self.filter_entries()
        if self.entry_tree.exists(key):
            self.entry_tree.selection_set(key)
            self.entry_tree.see(key)
        self.update_editor_title()
        self.mark_clean()
        self.set_status("status_entry_saved", key=key)
        logging.info("Entry saved: %s", key)
        if show_success:
            messagebox.showinfo(self.tr("info"), self.tr("msg_entry_saved", key=key))
        return True

    def save_xml_file(self):
        if not self.ensure_file_selected():
            return

        has_any_data = bool(self.entry_id_var.get().strip()) or any(self.collect_form_translations().values())
        if self.form_dirty and has_any_data:
            answer = messagebox.askyesnocancel(self.tr("confirm"), self.tr("msg_save_before_xml"))
            if answer is None:
                return
            if answer:
                if not self.save_entry(show_success=False):
                    return

        self.write_xml_to_path(self.xml_path)
        self.set_status("status_file_saved", path=self.xml_path)
        self.update_current_file_label()
        self.save_settings()
        logging.info("XML file saved: %s", self.xml_path)
        messagebox.showinfo(self.tr("info"), self.tr("msg_file_saved"))

    def save_xml_as(self):
        if not self.ensure_file_selected():
            return
        path = filedialog.asksaveasfilename(
            defaultextension=".xml",
            filetypes=[("XML files", "*.xml")],
            title=self.tr("menu_save_as"),
        )
        if not path:
            return
        self.write_xml_to_path(path)
        self.xml_path = path
        self.update_current_file_label()
        self.update_title()
        self.save_settings()
        self.set_status("status_file_saved", path=path)
        logging.info("XML file saved as: %s", path)

    def delete_selected_entry(self):
        selection = self.entry_tree.selection()
        key = selection[0] if selection else self.current_entry_id
        if not key:
            messagebox.showwarning(self.tr("warning"), self.tr("msg_nothing_selected"))
            return
        entry = self.get_entry_by_id(key)
        if not entry:
            return

        confirmed = messagebox.askyesno(self.tr("confirm"), self.tr("prompt_delete_entry", key=key))
        if not confirmed:
            return

        self.entries.remove(entry)
        if self.xml_path:
            self.write_xml_to_path(self.xml_path)
        if self.current_entry_id == key:
            self.clear_form(force=True)
        self.filter_entries()
        self.set_status("status_entry_deleted", key=key)
        logging.info("Entry deleted: %s", key)
        messagebox.showinfo(self.tr("info"), self.tr("msg_entry_deleted", key=key))

    def add_new_language(self):
        if not self.ensure_file_selected():
            return
        new_lang = simpledialog.askstring(self.tr("toolbar_add_language"), self.tr("prompt_language_code"), parent=self.root)
        if not new_lang:
            return
        new_lang = new_lang.strip()
        if not new_lang:
            return
        if new_lang in self.languages:
            messagebox.showwarning(self.tr("warning"), self.tr("msg_language_exists"))
            return

        existing_form = self.collect_form_translations()
        self.languages.append(new_lang)
        self.languages = sorted(set(self.languages), key=lambda value: (value != "en", value.lower()))
        self.refresh_language_panels()
        for lang, text in existing_form.items():
            widget = self.text_inputs.get(lang)
            if widget:
                widget.delete("1.0", tk.END)
                widget.insert("1.0", text)
        self.mark_dirty()
        self.set_status("status_language_added", lang=new_lang)
        messagebox.showinfo(self.tr("info"), self.tr("msg_language_added", lang=new_lang))
        logging.info("Language added to editor: %s", new_lang)

    def translate_text(self, source_text, source_lang, target_lang):
        if not self.translator_available or GoogleTranslator is None:
            raise RuntimeError(self.tr("msg_no_translator"))
        if source_lang == target_lang:
            return source_text
        translator = GoogleTranslator(source=source_lang, target=target_lang)
        return translator.translate(source_text)

    def create_progress_dialog(self, title, label_text, maximum):
        dialog = tk.Toplevel(self.root)
        dialog.title(title)
        dialog.geometry("430x140")
        dialog.resizable(False, False)
        dialog.transient(self.root)
        dialog.grab_set()
        dialog.configure(bg=self.colors["bg"])

        holder = ttk.Frame(dialog, style="Header.TFrame")
        holder.pack(fill="both", expand=True, padx=16, pady=16)

        label = ttk.Label(holder, text=label_text, style="Section.TLabel", wraplength=390, justify="left")
        label.pack(anchor="w")
        value_label = ttk.Label(holder, text="0 / 0", style="Info.TLabel")
        value_label.pack(anchor="w", pady=(10, 8))
        progress = ttk.Progressbar(holder, mode="determinate", maximum=max(1, maximum), value=0)
        progress.pack(fill="x")
        dialog.update_idletasks()
        return dialog, label, value_label, progress

    def auto_translate_current(self):
        if not self.translator_available:
            messagebox.showerror(self.tr("error"), self.tr("msg_no_translator"))
            return

        source_lang = self.source_lang_var.get().strip()
        if not source_lang or source_lang not in self.text_inputs:
            messagebox.showwarning(self.tr("warning"), self.tr("msg_missing_source_lang"))
            return

        source_text = self.text_inputs[source_lang].get("1.0", tk.END).strip()
        if not source_text:
            messagebox.showwarning(self.tr("warning"), self.tr("msg_missing_source"))
            return

        targets = [lang for lang in self.languages if lang != source_lang]
        if not targets:
            return

        dialog, label, value_label, progress = self.create_progress_dialog(
            self.tr("progress_title"),
            self.tr("progress_current_label"),
            len(targets),
        )
        label.configure(text=self.tr("progress_current_label"))

        errors = 0
        for index, lang in enumerate(targets, start=1):
            try:
                translated = self.translate_text(source_text, source_lang, lang)
                widget = self.text_inputs[lang]
                widget.delete("1.0", tk.END)
                widget.insert("1.0", translated)
            except Exception as exc:
                errors += 1
                logging.warning("Translation failed %s -> %s: %s", source_lang, lang, exc)
            progress.configure(value=index)
            value_label.configure(text=f"{index} / {len(targets)}")
            dialog.update_idletasks()

        dialog.destroy()
        self.mark_dirty()
        self.set_status("status_translation_done")
        if errors:
            messagebox.showwarning(self.tr("warning"), f"{self.tr('status_translation_done')}\nErrors: {errors}")
        logging.info("Current entry auto-translated from %s", source_lang)

    def add_language_and_translate_all(self):
        if not self.ensure_file_selected():
            return
        if not self.translator_available:
            messagebox.showerror(self.tr("error"), self.tr("msg_no_translator"))
            return
        if not self.entries:
            messagebox.showwarning(self.tr("warning"), self.tr("msg_no_entries"))
            return

        new_lang = simpledialog.askstring(
            self.tr("batch_translate"),
            self.tr("prompt_language_code_all"),
            parent=self.root,
        )
        if not new_lang:
            return
        new_lang = new_lang.strip()
        if not new_lang:
            return

        if new_lang in self.languages:
            confirm_replace = messagebox.askyesno(self.tr("confirm"), self.tr("prompt_replace_language", lang=new_lang))
            if not confirm_replace:
                return
        else:
            self.languages.append(new_lang)
            self.languages = sorted(set(self.languages), key=lambda value: (value != "en", value.lower()))

        source_lang = "en" if "en" in self.languages else self.languages[0]
        dialog, label, value_label, progress = self.create_progress_dialog(
            self.tr("progress_title"),
            self.tr("progress_batch_label", total=len(self.entries), lang=new_lang),
            len(self.entries),
        )
        label.configure(text=self.tr("progress_batch_label", total=len(self.entries), lang=new_lang))

        success = 0
        failed = 0
        for index, entry in enumerate(self.entries, start=1):
            source_text = (entry.get("translations", {}).get(source_lang) or "").strip()
            if not source_text:
                failed += 1
            else:
                try:
                    translated = self.translate_text(source_text, source_lang, new_lang)
                    entry.setdefault("translations", {})[new_lang] = translated
                    success += 1
                except Exception as exc:
                    failed += 1
                    logging.warning("Batch translation failed [%s] %s -> %s: %s", entry.get("id"), source_lang, new_lang, exc)
            progress.configure(value=index)
            value_label.configure(text=f"{index} / {len(self.entries)}")
            dialog.update_idletasks()

        dialog.destroy()
        self.refresh_language_panels()
        if self.current_entry_id:
            self.load_entry_into_form(self.current_entry_id)
        self.write_xml_to_path(self.xml_path)
        self.filter_entries()
        self.update_current_file_label()
        self.set_status("status_batch_done", lang=new_lang)
        logging.info("Batch translation completed for language: %s", new_lang)
        messagebox.showinfo(
            self.tr("info"),
            self.tr("msg_batch_finished", lang=new_lang, ok=success, failed=failed, total=len(self.entries)),
        )

    def show_about(self):
        messagebox.showinfo(self.tr("about_title"), self.tr("about_text"))

    def on_close(self):
        has_any_data = bool(self.entry_id_var.get().strip()) or any(self.collect_form_translations().values())
        if self.form_dirty and has_any_data:
            confirmed = messagebox.askyesno(self.tr("confirm"), self.tr("prompt_unsaved_exit"))
            if not confirmed:
                return
        self.save_settings()
        self.root.destroy()


def main():
    setup_logging()
    root = tk.Tk()
    app = LocalizationEditorApp(root)
    logging.info("Application started")
    root.mainloop()
    logging.info("Application closed")


if __name__ == "__main__":
    main()

