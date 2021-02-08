from recipes.models import User
from rest_framework.test import APITestCase


class CreateRecipeTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create(username='testuser',
                                        password='testpassword')
        # TODO understand why .login is not working here
        self.client.force_authenticate(user=self.user)

    def test_can_create_recipe(self):
        response = self.client.post('/api/recipes/',
                                    {'title': 'Grilled Cheese'},
                                    format='json')

        self.assertEqual(response.status_code, 201)
        self.assertEqual(
            self.user.recipes.filter(title='Grilled Cheese').count(), 1)

    def test_cannot_recipe_without_title(self):
        response = self.client.post('/api/recipes/', {}, format='json')

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data['title'], ["This field is required."])

    def test_can_create_recipe_with_ingredients(self):
        response = self.client.post('/api/recipes/', {
            'title':
            'Grilled Cheese',
            'ingredients': [{
                "amount": "2 slices",
                "item": "bread"
            }, {
                "amount": "1/2 stick",
                "item": "butter"
            }],
        },
                                    format='json')
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data['user'], 'testuser')
        self.assertEqual(len(response.data['ingredients']), 2)
        self.assertEqual(response.data['ingredients'][0]['item'], 'bread')

        new_recipe = self.user.recipes.get(title='Grilled Cheese')
        self.assertEqual(new_recipe.ingredients.count(), 2)
