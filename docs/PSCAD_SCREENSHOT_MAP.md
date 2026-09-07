# Guia para substituir desenhos por capturas do PSCAD

Localizacoes verificadas no codigo em 2026-09-07. Os numeros de imagem referem-se aos arquivos extraidos de sugestoes-para-manim.docx em docs/source_review. As linhas correspondem a esta revisao; os nomes das classes e funcoes sao os localizadores estaveis.

| Imagem do documento | Cena | Criacao e posicionamento | Desenho reutilizavel |
|---|---|---|---|
| image7.png | `CreateComponentScene` | [pscad_rectifier_presentation.py:352](../pscad_rectifier_presentation.py#L352) | [pscad_visuals.py:268](../pscad_visuals.py#L268) (`capacitor_symbol`) |
| image8.png | `RectifierConstructionScene` | [pscad_rectifier_presentation.py:452](../pscad_rectifier_presentation.py#L452) | [pscad_visuals.py:301](../pscad_visuals.py#L301) (`make_rectifier_bridge`) |
| image8.png | `RectifierOperationScene` | [pscad_rectifier_presentation.py:479](../pscad_rectifier_presentation.py#L479) | [pscad_visuals.py:301](../pscad_visuals.py#L301) (`make_rectifier_bridge`) |
| image9.png | `SourceCreationScene` | [pscad_rectifier_presentation.py:425](../pscad_rectifier_presentation.py#L425) | [pscad_visuals.py:211](../pscad_visuals.py#L211) (`source_symbol`) |
| image10.png | `DCFilterScene` | [pscad_rectifier_presentation.py:505](../pscad_rectifier_presentation.py#L505) | [pscad_visuals.py:337](../pscad_visuals.py#L337) (`dc_parallel_load`) |

## Como substituir

Guarde as capturas em `assets/pscad/`, por exemplo `capacitor.png`, `rectifier_bridge.png`, `three_phase_source.png` e `dc_load.png`. Nenhuma captura foi inventada nem substituida nesta revisao: o pedido foi indicar os pontos de edicao.

Na cena, importe `ImageMobject` de Manim e `Path` de pathlib. Substitua a chamada do helper pela leitura da imagem, mantenha a variavel e ajuste sua caixa antes de posicionar:

```python
image_path = Path(__file__).resolve().parent / "assets" / "pscad" / "capacitor.png"
cap = ImageMobject(str(image_path))
fit_to_box(cap, 3.0, 1.4)
cap.move_to(np.array([3.4, -1.75, 0]))
```

`CreateComponentScene` anima `cap` por FadeIn/Circumscribe, portanto aceita a imagem. `SourceCreationScene` e `DCFilterScene` tambem usam FadeIn. Em `RectifierConstructionScene`, substitua a animacao por partes (`bridge[:6]`, `bridge[6:]`, Create) por `self.play(FadeIn(bridge))`: uma captura raster nao possui os seis diodos como subobjetos. Em `RectifierOperationScene`, reposicione o caminho verde de corrente para coincidir com os terminais na captura.

Nao coloque ImageMobject dentro de VGroup: use Group se precisar agrupar raster e vetores. Mantenha proporcao e enquadramento, e renderize a cena depois de cada troca.

Os icones da coluna central de FullWorkflowScene agora sao independentes desses helpers: procure `steps` dentro da classe e `workflow_icon` em pscad_visuals.py. Alterar o helper de ponte ou carga nao modifica esses icones.
