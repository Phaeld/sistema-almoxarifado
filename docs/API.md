# API Central (Multi-Maquina)

Esta API permite que 2-3 maquinas usem o mesmo banco de dados central.

## 1) Instalar dependencias

```powershell
pip install -r requirements.txt
```

## 2) Configurar variaveis (opcional)

```powershell
$env:ALMOX_API_HOST="0.0.0.0"
$env:ALMOX_API_PORT="8000"
$env:ALMOX_API_DEBUG="1"
$env:ALMOX_API_KEY="troque-esta-chave"
```

Se `ALMOX_API_KEY` estiver vazio, a API nao exige chave.

## 3) Executar

```powershell
python -m src.api
```

## 4) Acessar documentacao

- Swagger: `http://SEU_IP:8000/docs`
- Healthcheck: `http://SEU_IP:8000/health`

## Endpoints iniciais

- `POST /auth/login`
- `GET /users`
- `GET /users/{username}/exists`
- `POST /users`
- `PUT /users/{user_id}`
- `DELETE /users/{user_id}`
- `PATCH /users/{username}/image`
- `GET /materials`
- `POST /materials`
- `PATCH /materials/{id_item}/quantity`
- `GET /actions`
- `GET /actions/next-id/{prefix}`
- `GET /actions/{id_action}`
- `POST /actions`
- `PATCH /actions/{id_action}/status`
- `GET /vehicles`
- `GET /vehicles/by-plate`
- `GET /vehicles/{vehicle_id}`
- `POST /vehicles`
- `PUT /vehicles/{vehicle_id}`
- `DELETE /vehicles/{vehicle_id}`
- `GET /vehicles/distinct/fuel-types`
- `GET /vehicles/distinct/odometer-types`
- `GET /controls`
- `GET /controls/{control_id}`
- `GET /controls/last-by-plate`
- `POST /controls`
- `PUT /controls/{control_id}`
- `DELETE /controls/{control_id}`
- `GET /controls/distinct/fuel-types`

## Proximo passo no cliente desktop

No cliente (cada maquina), configure:

```powershell
$env:ALMOX_API_BASE_URL="http://IP_DO_SERVIDOR:8000"
$env:ALMOX_API_KEY="troque-esta-chave"
```

Com isso, os services do app passam a usar a API automaticamente.
