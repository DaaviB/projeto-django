from authors.forms import AuthorRecipeForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http.response import Http404
from django.shortcuts import redirect, render
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views import View
from recipes.models import Recipe


@method_decorator(login_required(
    login_url='authors:login', redirect_field_name='next',
), name='dispatch')
class DashboardRecipe(View):
    def get_recipe(self, id=None):
        recipe = None

        if id is not None:
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

    @method_decorator(login_required(
        login_url='authors:login', redirect_field_name='next'
    ))
    def get(self, request, id=None):
        recipe = self.get_recipe(id)

        form = AuthorRecipeForm(instance=recipe)

        return self.render_recipe(form, recipe)

    @method_decorator(login_required(
        login_url='authors:login', redirect_field_name='next'
    ))
    def post(self, request, id=None):
        recipe = self.get_recipe(id)

        form = AuthorRecipeForm(
            data=request.POST or None,
            files=request.FILES or None,
            instance=recipe
        )

        if form.is_valid():
            recipe = form.save(commit=False)
            recipe.author = request.user
            recipe.preparation_steps_is_html = False
            recipe.is_published = False

            recipe.save()

            messages.success(request, 'Sua receita foi salva com sucesso.')
            return redirect(
                reverse(
                    'authors:dashboard',
                )
            )

        return self.render_recipe(form, recipe)
