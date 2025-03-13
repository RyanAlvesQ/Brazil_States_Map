window.onload = function() {
    let map = L.map('map').setView([-14.2350, -51.9253], 4);
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png').addTo(map);
    let estadoLayer;

    fetch('/estados')
        .then(response => response.json())
        .then(data => {
            let select = document.getElementById('estadoSelect');
            data.estados.forEach(estado => {
                let option = document.createElement('option');
                option.value = estado;
                option.textContent = estado;
                select.appendChild(option);
            });
        });

    document.getElementById('estadoSelect').addEventListener('change', function() {
        let estado = this.value;
        if (estado) {
            fetch(`/estado?nome=${estado}`)
                .then(response => response.json())
                .then(data => {
                    if (estadoLayer) {
                        map.removeLayer(estadoLayer);
                    }
                    estadoLayer = L.geoJSON(JSON.parse(data.geojson), {
                        style: { color: '#89AC46', weight: 2 }
                    }).addTo(map);
                    map.fitBounds(estadoLayer.getBounds());
                });
        }
    });
}

function enviarDados() {
    let nome = document.getElementById('nomeUsuario').value;
    let estado = document.getElementById('estadoSelect').value;
    
    if (nome.trim() === "" || estado.trim() === "") {
        alert("Por favor, digite seu nome e selecione o estado que você mora.");
        return;
    }

    console.log('Enviando dados:', { nome: nome, estado: estado });

    fetch('/salvar_dados', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ nome: nome, estado: estado })
    })
    .then(response => response.json())
    .then(data => {
        alert(data.mensagem);
        console.log('Resposta do servidor:', data);
    })
    .catch(error => {
        console.error('Erro:', error);
        alert('Erro ao salvar os dados!');
    });
}
