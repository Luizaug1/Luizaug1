# Deploy Garden · assets

Identidade em verde fósforo e pixel art, inspirada na grade de contribuições do GitHub.

| Arquivo | Função |
| --- | --- |
| `deploy-garden-header.png` | Cabeçalho do perfil, 1000 × 260. |
| `deploy-snake.gif` | Animação principal, 1000 × 250, loop infinito. |
| `deploy-snake-preview.png` | Quadro estático para inspeção. |
| `generate.py` | Gerador determinístico com Pillow. |
| `requirements.txt` | Dependência para reprodução. |

Na raiz do repositório:

```bash
python -m pip install -r assets/requirements.txt
python assets/generate.py
```

A animação é ilustrativa: não consulta APIs nem acompanha deploys reais. Cada coleta gera um alvo alcançável; a busca em largura evita o corpo da cobra. A semente fixa torna o resultado reproduzível. Um GIF sempre repete: o ciclo longo e a transição final suavizam a repetição.
