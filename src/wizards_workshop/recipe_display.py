from ursina import *


class RecipeDisplay(Entity):
    def __init__(self, recipe_book):
        super().__init__()
        self.recipe_book = recipe_book
        self.current_page = 0
        self.recipes_per_page = 4
        
        self.setup_ui()
        
    def setup_ui(self):
        # Background panel
        self.panel = Entity(
            parent=camera.ui,
            model="quad",
            color=color.dark_gray,
            scale=(0.3, 0.4, 1),
            position=(0.7, 0, 0),
            alpha=0.9
        )
        
        # Title
        self.title = Text(
            text="Recipe Book",
            parent=self.panel,
            position=(0, 0.18, -0.01),
            scale=3,
            origin=(0, 0),
            color=color.white
        )
        
        # Recipe texts
        self.recipe_texts = []
        for i in range(self.recipes_per_page):
            recipe_text = Text(
                parent=self.panel,
                position=(-0.14, 0.12 - i * 0.08, -0.01),
                scale=1.5,
                origin=(-0.5, 0),
                color=color.light_gray
            )
            self.recipe_texts.append(recipe_text)
            
        # Navigation
        self.prev_button = Button(
            text="Prev",
            parent=self.panel,
            scale=(0.08, 0.05),
            position=(-0.1, -0.18, -0.01),
            on_click=self.prev_page
        )
        
        self.next_button = Button(
            text="Next",
            parent=self.panel,
            scale=(0.08, 0.05),
            position=(0.1, -0.18, -0.01),
            on_click=self.next_page
        )
        
        self.page_text = Text(
            parent=self.panel,
            position=(0, -0.18, -0.01),
            scale=1.5,
            origin=(0, 0),
            color=color.white
        )
        
        self.update_display()
        
    def update_display(self):
        all_recipes = self.recipe_book.recipes
        total_pages = (len(all_recipes) - 1) // self.recipes_per_page + 1
        
        start_idx = self.current_page * self.recipes_per_page
        end_idx = min(start_idx + self.recipes_per_page, len(all_recipes))
        
        # Clear all recipe texts
        for text in self.recipe_texts:
            text.text = ""
            
        # Display recipes for current page
        for i, recipe_idx in enumerate(range(start_idx, end_idx)):
            recipe = all_recipes[recipe_idx]
            ingredients = " + ".join(recipe.inputs)
            self.recipe_texts[i].text = f"{recipe.verb}: {ingredients} → {recipe.output}"
            
        # Update page indicator
        self.page_text.text = f"{self.current_page + 1}/{total_pages}"
        
        # Update button states
        self.prev_button.disabled = self.current_page == 0
        self.next_button.disabled = self.current_page >= total_pages - 1
        
    def prev_page(self):
        if self.current_page > 0:
            self.current_page -= 1
            self.update_display()
            
    def next_page(self):
        total_pages = (len(self.recipe_book.recipes) - 1) // self.recipes_per_page + 1
        if self.current_page < total_pages - 1:
            self.current_page += 1
            self.update_display()
            
    def toggle_visibility(self):
        self.panel.enabled = not self.panel.enabled