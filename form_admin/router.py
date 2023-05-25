from typing import List
from fastapi import APIRouter
from form_admin.schemas import Form as FormSchema, CreateForm, FormSettings, Route, FormTemplate, FormTemplateCreate


router = APIRouter()


@router.get("/", response_model=List[FormSchema])
def all_forms_page():
    pass


@router.post("/new-form", response_model=CreateForm)
def create_form():
    pass


@router.get("/{form_id}", response_model=FormSchema)
def read_form():
    pass


@router.delete("/{form_id}")
def delete_form(form_id: int):
    return {"status": 200, "message": "Form deleted"}


@router.get("/{form_id}/settings", response_model=FormSettings)
def read_form_settings(form_id: int):
    return {
              "name": "Orders",
              "icon": "favicon1.png",
              "icon_color": "blue",
              "folder": "Desktop",
              "template": "",
              "print_templates": [
                {"file": "Company_Order_blank.docx"}
              ]
            }


@router.put("/{form_id}/settings", response_model=FormSettings)
def update_form_settings(form_id: int):
    return read_form_settings(form_id)


@router.get("/{form_id}/template", response_model=FormTemplate)
def read_form_template():
    return {
        "fields": [
            {
            "id": 1,
            "type": "text",
            "in_title": False,
            "visible_on_step": 1,
            "required_on_step": 0,
            "immutable_from_step": 0,
            "show_if": {}
            },
        ]
    }


@router.post("/{form_id}/template", response_model=FormTemplateCreate)
def create_form_template():
    return {
        "fields": [
            {}
        ]
    }


@router.put("/{form_id}/template")
def update_form_template():
    pass


@router.get("/{form_id}/access")
def read_form_access():
    pass


@router.put("/{form_id}/access")
def update_form_access():
    pass


@router.get("/{form_id}/routes", response_model=Route)
def read_form_routes(form_id: int):
    return {
            "steps": [
                    {
                        "step_id": 1,
                        "step_name": "New order",
                        "responsible": ["Pavl Sev", "And Pop"]
                    },
                    {
                        "step_id": 2,
                        "step_name": "Order Confirmed",
                        "responsible": ["Pavl Sev"]
                    }
              ]
            }


@router.put("/{form_id}/routes", response_model=Route)
def update_form_routes(form_id: int):
    return {"status": 200, "message": "Routes updated successfully"}


@router.get("/{form_id}/extensions")
def read_form_extensions():
    pass


@router.put("/{form_id}/extensions")
def update_form_extensions():
    pass

