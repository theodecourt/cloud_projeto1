# Documentação
#### Theo Decourt

[Link do Docker Hub](https://hub.docker.com/r/theodecourt/projeto11)

[Link do Video](https://youtu.be/ThNbsf5nexE)

## Docker Compose
**Baixe o docker-compose.yml:**
<a href="https://github.com/theodecourt/cloud_projeto1/blob/main/docker-compose.yml" id="downloadLink">docker-compose.yml</a>

<script>
document.getElementById('downloadLink').addEventListener('click', function(event) {
    event.preventDefault();
    const url = 'https://raw.githubusercontent.com/theodecourt/cloud_projeto1/main/docker-compose.yml';
    const fileName = 'docker-compose.yml';

    fetch(url)
    .then(response => response.blob())
    .then(blob => {
        const link = document.createElement('a');
        link.href = window.URL.createObjectURL(blob);
        link.download = fileName;
        link.click();
    })
    .catch(error => {
        console.error('Erro ao baixar o arquivo:', error);
        alert('Falha ao baixar o arquivo.');
    });
});
</script>

## Funcionamento do Projeto

##### 1. Rodar Container
```bash
docker compose up
```

#### 2. Acesse a documentação da API em:
```bash
http://localhost:8000/docs
```

##### 3. Cadastre um novo usuário
```bash
{
  "nome": "string",
  "email": "string",
  "senha": "string"
}
```
Se der tudo certo o cadastro deverá gerar um código jwt:
```bash
{
  "jwt": <seu_codigo_jwt>
}
```
Copie seu código jwt. Deixe ele bem guardado pois usaremos mais para frente.

##### 4. Faça login
```bash
{
  "email": "string",
  "senha": "string"
}
```
Se o login for bem sucedido ele deverá gerar um código jwt:

```bash
{
  "jwt": <seu_codigo_jwt>
}
```

##### Acesse o Endpoint: GET /consultar
Este endpoint permite ao cliente consultar informações específicas protegidas por autenticação JWT.

Para acessar é necessário primeiro autenticar com o JWT:
```bash
eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```
Sendo o teken sua chave <jwt>

Se o Token for validado deverá aparecer uma lista com as conversões de moedas assim:
```
{
  "USD": 1,
  "AED": 3.6725,
  "AFN": 66.747,
  "ALL": 91.3568,
  "AMD": 387.4389,
  "ANG": 1.79,
  "AOA": 918.7449,
  "ARS": 985.92,
  "AUD": 1.5065,
  "AWG": 1.79,
  "AZN": 1.7008,
  "BAM": 1.814,
  "BBD": 2,
  "BDT": 119.466,
  "BGN": 1.8142,
  "BHD": 0.376,
  "BIF": 2904.6033,
  "BMD": 1,
  "BND": 1.3224,
  "BOB": 6.9143,
  "BRL": 5.698,
  ...
}
```

##### 6. Para finalizar, execute o comando abaixo:
```
docker compose down
```

# Para buildar a imagem

### Buildando a imagem em ambas as arquiteturas (x86 e ARM)

Rodar os seguintes comandos:
```
# Ativar o buildx
docker buildx create --use

# Resetar o buildx
docker run --rm --privileged multiarch/qemu-user-static --reset -p yes

# Construir a imagem em ambas as arquiteturas e enviar para o Docker Hub
docker buildx build --platform linux/amd64,linux/arm64 -t theodecourt/projeto11:latest . --push
```
No último comando é necessario colocar o seu_usuario/sua_imagem