from locust import HttpUser, task, between

class ECommerceUser(HttpUser):
    # Define o "think time" (tempo de espera) do usuário entre 1 e 3 segundos
    wait_time = between(1, 3)

    @task(10) # 10x mais provável de executar
    def view_product(self):
        """ Simula a visualização de um produto """
        self.client.get(f"/produto/1", name="/produto/[id]")

    @task(5) # 5x mais provável
    def view_category(self):
        """ Simula a visualização de uma categoria """
        self.client.get("/categoria/promocoes", name="/categoria/[nome]")

    @task(2) # 2x mais provável
    def add_to_cart(self):
        """ Simula a adição de um item ao carrinho """
        self.client.post("/api/carrinho/add", json={"id": 1}, name="/api/carrinho/add")

    @task(1) # Menos provável
    def checkout(self):
        """ Simula a visita à página de checkout """
        self.client.get("/checkout", name="/checkout")