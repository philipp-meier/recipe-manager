interface IRecipe {
    pk: number;
    name: string;
    category: string;
    img: string;    
}

document.addEventListener("DOMContentLoaded", () => new RecipeList());

class RecipeList {
    private current_page = 1;

    constructor() {
        // Preload the first page.
        this.loadRecipes(1);
    }

    private loadRecipes(pageNum: number): void {
        const paginationContainer = <HTMLElement>document.querySelector(".pagination");

        // Remove existing pagination items
        paginationContainer.replaceChildren();

        let recipeApiUrl = `/api/v1/recipes/${pageNum}`;
        const textfilter = (<any>window).textfilter;
        if (textfilter)
            recipeApiUrl += `?q=${textfilter}`;

        fetch(recipeApiUrl)
            .then(response => response.json())
            .then(result => {
                const curPage = result.curPage;

                // Previous button
                paginationContainer.append(this.createPaginationItem(window.gettext('Previous'), curPage-1, !result.hasPrevious));

                // Add the refreshed pagination items
                for (let i = 1; i <= result.numPages; i++) {
                    const paginationItem = this.createPaginationItem(i.toString(), i);

                    if (i == curPage)
                        paginationItem.classList.add("active");

                    paginationContainer.append(paginationItem);
                }

                // Next button
                paginationContainer.append(this.createPaginationItem(window.gettext('Next'), curPage+1, !result.hasNext));

                const recipeContainer = <HTMLDivElement>document.querySelector("#recipes");
                // Remove all recipes from the previous page
                recipeContainer.replaceChildren();

                const recipes = <IRecipe[]>result.recipes;
                for (let i = 0; i < recipes.length; i++)
                    recipeContainer.append(this.createRecipeContainer(recipes[i]));

                this.current_page = curPage;
            });
    }

    private createRecipeContainer(recipe: IRecipe): HTMLDivElement {
        const container = document.createElement('div');
        container.className = "recipe-list-item-container border border-black rounded-3 mb-2";

        const listItem = document.createElement('div');
        listItem.className = "recipe-list-item";
        container.append(listItem);

        const imageContainer = document.createElement('div');
        imageContainer.className = "recipe-image-container";
        listItem.append(imageContainer);

        if (recipe.img) {
            const img = document.createElement('img');
            img.src = recipe.img;
            imageContainer.append(img);
        }
        else {
            const p = document.createElement('p');
            p.textContent = window.gettext("ImageNotAvailable");
            imageContainer.append(p);
        }

        const detailsContainer = document.createElement('div');
        detailsContainer.className = "recipe-details";
        listItem.append(detailsContainer);

        const title = document.createElement('span');
        title.className = "title";
        title.textContent = recipe.name;
        detailsContainer.append(title);

        const category = document.createElement('p');
        category.textContent = recipe.category;
        detailsContainer.append(category);

        const commandContainer = document.createElement('div');
        commandContainer.className = "commands";
        detailsContainer.append(commandContainer);

        const viewLink = document.createElement('a');
        viewLink.className = "btn btn-sm btn-outline-primary";
        viewLink.href = `/recipe/edit/${recipe.pk}`;
        viewLink.innerHTML = `<i class="bi-search"></i> ${window.gettext('ViewRecipe')}`;
        commandContainer.append(viewLink);

        const deleteButton = document.createElement('button');
        deleteButton.className = "btn btn-sm btn-outline-danger mx-1";
        deleteButton.innerHTML = `<i class='bi-trash'></i> ${window.gettext('Delete')}`;
        deleteButton.onclick = () => {
            fetch("/api/v1/recipe", {
                method: "DELETE",
                body: JSON.stringify({ id: recipe.pk })
            })
            .then(response => {
                if (response.status === 200) {
                    container.style.animationPlayState = "running";
                    container.addEventListener("animationend", () => {
                        // Reload current page.
                        this.loadRecipes(this.current_page);
                    });
                }
            });
        };
        commandContainer.append(deleteButton);

        return container;
    }

    private createPaginationItem(text: string, pageNum: number, disableState = false): HTMLLIElement {
        const li = document.createElement('li');
        li.classList.add("page-item");

        const button = document.createElement('button');

        if (!disableState)
            button.onclick = () => this.loadRecipes(pageNum);
        else
            button.classList.add("disabled");

        button.classList.add("page-link");
        button.innerText = text;

        li.append(button);

        return li;
    }
}

