from authors.forms import AuthorRecipeForm
from django.contrib import messages
from django.http.response import Http404
from django.shortcuts import redirect, render
from django.urls import reverse
from django.views import View
from recipes.models import Recipe


class DashboardRecipe(View):
    def get_recipe(self, id):
        recipe = None

        if id:
            recipe = Recipe.objects.filter(
                is_published=False,
                author=self.request.user,
                pk=id,
            ).first()

            if not recipe:
                raise Http404()

        return recipe

    def render_recipe(self, form, recipe):
        return render(
            self.request,
            'authors/pages/dashboard_recipe.html',
            context={

                'form': form,
                'recipe': recipe,
            })

    def get(self, request, id):
        recipe = self.get_recipe(id)

        form = AuthorRecipeForm(instance=recipe)

        return self.render_recipe(form, recipe)

    def post(self, request, id):
        recipe = self.get_recipe(id)

        form = AuthorRecipeForm(
            data=request.POST or None,
            files=request.FILES or None,
            instance=recipe
        )

        if form.is_valid():
            form = form.save(commit=False)
            form.author = request.user
            form.preparation_steps_is_html = False
            form.is_published = False

            form.save()

            messages.success(request, 'Sua receita foi salva com sucesso.')
            return redirect(
                reverse(
                    'authors:dashboard_recipe_edit', args=(id,))
            )

        return self.render_recipe(form, recipe)
