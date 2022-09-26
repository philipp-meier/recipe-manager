interface IIngredient {
    amount: string;
    unit: string;
    ingredient: string;
}

window.addEventListener("DOMContentLoaded", () => {
    const container = <HTMLDivElement>document.querySelector("#ingredientsControl");
    const ctrl = new IngredientsControl(container);
    ctrl.create();

    (<HTMLButtonElement>document.querySelector("#recipeForm")).onsubmit = () => {
        ctrl.setPostData();
        return true;
    };
});

class IngredientsControl {
    private _parent: Element;
    private _ctl: Element | undefined;
    private _items: IIngredient[];

    constructor(p: Element) {
        this._parent = p;
        this._items = (<any>window).recipeIngredients || [];
    }

    public create(): void {
        const ctl = document.createElement('div');

        const btnAddIngredient = document.createElement('btn');
        btnAddIngredient.className = "btn btn-sm btn-outline-success";
        btnAddIngredient.innerHTML = `<i class='bi-plus-circle'></i> ${window.gettext("AddIngredient")}`;
        btnAddIngredient.onclick = () => this.addIngredientRow(<HTMLElement>ctl.querySelector("tbody"));
        ctl.append(btnAddIngredient);

        const table = document.createElement('table');
        table.className = "table";

        table.append(this.buildTableHeader());
        table.append(this.buildTableBody());

        const tableContainer = document.createElement('div');
        tableContainer.className = 'table-responsive-lg';
        tableContainer.append(table);

        ctl.append(tableContainer);
        this._parent.append(ctl);

        this._ctl = ctl;
    }

    private buildTableHeader(): HTMLElement {
        const thead = document.createElement('thead');

        const tr = document.createElement('tr');
        ["Amount", "Unit", "Ingredient", "Commands"].forEach(text => {
            const th = document.createElement('th');
            th.scope = "col";
            th.textContent = window.gettext(text);

            tr.append(th);
        });

        thead.append(tr);
        return thead;
    }

    private buildTableBody(): HTMLElement {
        const tbody = document.createElement('tbody');
        this._items.forEach(item => this.addIngredientRow(tbody, item));

        return tbody;
    }
    private addIngredientRow(tbody: Element, item: IIngredient | undefined = undefined): void {
        const tr = document.createElement('tr');

        const tdAmount = document.createElement('td');
        const inputAmount = document.createElement('input');
        inputAmount.type = "text";
        inputAmount.value = item?.amount || "";
        tdAmount.append(inputAmount);

        const tdUnit = document.createElement('td');
        const inputUnit = document.createElement('input');
        inputUnit.type = "text";
        inputUnit.value = item?.unit || "";
        tdUnit.append(inputUnit);

        const tdIngredient = document.createElement('td');
        const inputIngredient = document.createElement('input');
        inputIngredient.type = "text";
        inputIngredient.value = item?.ingredient || "";
        inputIngredient.onkeydown = (ev) => {
            // So that the user can add a new row without clicking on "Add ingredients" every time.
            if (ev.key === "Tab" && tbody.lastChild === (<HTMLElement>ev.target).parentElement?.parentElement) {
                this.addIngredientRow(tbody);
            }
        };
        tdIngredient.append(inputIngredient);

        const tdCommands = document.createElement('td');
        const btnDelete = document.createElement('button');
        btnDelete.innerHTML = `<i class='bi-trash'></i> ${window.gettext("Delete")}`;
        btnDelete.className = "btn btn-sm btn-outline-danger";
        btnDelete.type = "button";
        btnDelete.tabIndex = -1;
        btnDelete.onclick = () => tr.remove();
        tdCommands.append(btnDelete);

        tr.append(tdAmount);
        tr.append(tdUnit);
        tr.append(tdIngredient);
        tr.append(tdCommands);

        tbody.append(tr);
    }

    public setPostData(): void {
        if (!this._ctl)
            return;

        const container = document.createElement('div');
        const postData = document.createElement('input');
        postData.type = "hidden";
        postData.name = "ingredients";
        postData.value = this.serializeIngredients();

        container.append(postData);
        this._ctl.append(container);
    }

    private serializeIngredients(): string {
        if (!this._ctl)
            return "";

        const ingredients: IIngredient[] = [];
        this._ctl.querySelectorAll("table > tbody > tr").forEach(tr => {
            const cols = tr.children,
                amount = (<HTMLInputElement>cols[0].firstChild).value,
                unit = (<HTMLInputElement>cols[1].firstChild).value,
                ingredient = (<HTMLInputElement>cols[2].firstChild).value;

            if (amount && unit && ingredient)
                ingredients.push({ amount: amount, unit: unit, ingredient: ingredient });
        });

        return JSON.stringify(ingredients);
    }
}