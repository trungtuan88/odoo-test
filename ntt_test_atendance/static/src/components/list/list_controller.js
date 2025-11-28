import { _t } from "@web/core/l10n/translation";
import { ListController } from '@web/views/list/list_controller';
import { listView } from "@web/views/list/list_view";
import { registry } from "@web/core/registry";
import { deleteConfirmationMessage } from "../delete_confirmation_message";

export class DeleteConfirmationListController extends ListController {

    get deleteConfirmationDialogProps() {
        const root = this.model.root;
        const res = super.deleteConfirmationDialogProps;
        if (root.isDomainSelected || root.selection.length > 1) {
            res.body += "\n\n" + _t("If you 'Delete' these records, the system will automatically create a deletion request for these records on the device.");
        } else {
            res.body = deleteConfirmationMessage;
        }
        return res;
    }
}

export const DeleteConfirmationListView = {
    ...listView,
    Controller: DeleteConfirmationListController,
};

registry.category("views").add("delete_confirmation_list", DeleteConfirmationListView);
