# Documenteaação
#### Theo Decourt

[Link do Docker Hub](https://hub.docker.com/r/theodecourt/fast_app-app)

## Docker Compose
**Baixe o docker-compose.yml:**
<a href="https://github.com/theodecourt/cloud_projeto1/blob/main/docker-compose.yml" id="downloadLink">docker-compose.yml</a>

<script>
document.getElementById('downloadLink').addEventListener('click', function(event) {
    event.preventDefault();
    const url = this.href;
    const fileName = 'docker-compose.yml';

    fetch(url)
    .then(response => response.blob())
    .then(blob => {
        const link = document.createElement('a');
        link.href = window.URL.createObjectURL(blob);
        link.download = fileName;
        link.click();
    })
    .catch(() => alert('Falha ao baixar o arquivo.'));
});
</script>

