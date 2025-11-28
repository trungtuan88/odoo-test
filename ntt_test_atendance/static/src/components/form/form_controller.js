import { _t } from "@web/core/l10n/translation";
import { FormController } from '@web/views/form/form_controller';
import { formView } from "@web/views/form/form_view";
import { registry } from "@web/core/registry";
import { deleteConfirmationMessage } from "../delete_confirmation_message";

export class DeleteConfirmationFormController extends FormController {

    get deleteConfirmationDialogProps() {
        const res = super.deleteConfirmationDialogProps;
        res.body = deleteConfirmationMessage;
        return res;
    }
}

export const DeleteConfirmationFormView = {
    ...formView,
    Controller: DeleteConfirmationFormController,
};

registry.category("views").add("delete_confirmation_form", DeleteConfirmationFormView);