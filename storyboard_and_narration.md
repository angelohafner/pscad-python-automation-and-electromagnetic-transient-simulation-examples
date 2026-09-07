# Complete Storyboard and Narration — PSCAD Automation with Python

## Presentation target

- Format: Manim Community Edition, 16:9
- Default render: 854×480, 15 fps; optional Full HD
- Language on screen: English with original Python/API names preserved
- Narration: Brazilian Portuguese
- Narration timing below is a planning aid; actual silent MP4 duration comes from ffprobe
- Source script: `three_phase_rectifier_fft_pscad.py`
- Principle: **Code → Meaning → Visual Action**

---

## Scene 01 — IntroScene

**Objective:** Establish the complete learning path.

**Visuals:** Large title; horizontal pipeline Python → PSCAD → EMT → Data → FFT → Harmonics + THD; offline vector icons.

**Code shown:** none.

**Animation:** Blocks appear sequentially and arrows connect them.

**Narration:**

> Nesta apresentação vamos acompanhar um script Python que automatiza um estudo completo no PSCAD. O exemplo constrói um retificador trifásico de seis pulsos, executa a simulação EMT, recupera as correntes e realiza a análise harmônica da fase A. O ponto central é acompanhar o caminho completo: do código Python até os resultados de engenharia.

**Duration:** 18 s.

---

## Scene 02 — ManualVsAutomationScene

**Objective:** Explain what automation replaces and what it does not replace.

**Visuals:** Manual workflow on the left; Python → PSCAD → EMTDC on the right.

**Code shown:** conceptual `Python script` only.

**Animation:** Manual steps accumulate; automated pipeline replaces them.

**Narration:**

> Sem automação, o engenheiro abriria o PSCAD, criaria o case, procuraria cada componente, posicionaria, configuraria, conectaria e depois executaria o estudo. O Python automatiza essas tarefas repetitivas. Mas ele não substitui o PSCAD: o solver EMT continua sendo o responsável pela solução numérica do circuito.

**Duration:** 24 s.

---

## Scene 03 — ArchitectureScene

**Objective:** Separate automation, simulation, and post-processing.

**Visuals:** Left column Python → mhi.pscad → Automation Library → PSCAD → EMTDC; right column OUT/INF → OutFile → NumPy → FFT → THD.

**Code shown:** `mhi.pscad` and `OutFile` concepts.

**Narration:**

> O exemplo tem três camadas. A primeira é a automação, feita em Python com a biblioteca `mhi.pscad`. A segunda é a simulação eletromagnética propriamente dita, executada pelo PSCAD e pelo EMTDC. A terceira volta ao Python, que lê os arquivos de saída e calcula FFT, harmônicos e THD.

**Duration:** 24 s.

---

## Scene 04 — ScriptOverviewScene

**Objective:** Present the exact `main()` sequence.

**Visuals:** 11 stage blocks following the real program order.

**Code shown:** function names from `main()`.

**Animation:** Each stage is highlighted as if the script were executing.

**Narration:**

> O `main()` do programa funciona como um roteiro. Primeiro ele inicia o PSCAD e prepara o projeto. Depois cria o circuito, as medições e os gráficos. Em seguida executa o PSCAD, transforma a saída em CSV e finalmente entra no pós-processamento: FFT, harmônicos, THD, figuras e arquivos de resumo.

**Duration:** 28 s.

---

## Scene 05 — WorkspaceScene

**Objective:** Explain workspace/case creation and loading.

**Visuals:** Code left; decision flow right.

**Code shown:** `WORKSPACE_PATH.is_file()`, `pscad.load`, `new_workspace`, `create_case`.

**Narration:**

> A função `create_or_load_project` permite duas situações. Se o workspace já existir, o script carrega o arquivo e procura o case pelo nome. Caso contrário, cria um novo workspace e um novo case. Esse case será o contêiner da simulação e dele obtemos o canvas principal.

**Duration:** 26 s.

---

## Scene 06 — ComponentLibraryScene

**Objective:** Explain scoped Master Library definitions.

**Visuals:** Catalog cards for `source3`, `breakout`, `peswitch`, `capacitor`, `pgb`, `datalabel`.

**Code shown:** scoped names.

**Narration:**

> Uma string como `master:capacitor` não é ainda um capacitor no diagrama. Ela identifica uma definição da biblioteca Master do PSCAD. Os catálogos anexos confirmam essas definições e suas descrições. A instância só aparece no schematic quando o Python chama `canvas.create_component`.

**Duration:** 28 s.

---

## Scene 07 — CreateComponentScene

**Objective:** Explain the generic component factory helper.

**Visuals:** Code panel → definition + position → capacitor instance.

**Code shown:** `create_component()`.

**Narration:**

> Esta função auxiliar concentra a ação mais repetida do projeto. Ela recebe a definição do componente, extrai as coordenadas `x` e `y` e pede ao canvas que crie a instância. Assim, o código pode tratar fonte, diodo, resistor, capacitor e medidores de maneira uniforme.

**Duration:** 22 s.

---

## Scene 08 — CoordinateAndPortsScene

**Objective:** Explain why geometry and ports matter.

**Visuals:** PSCAD-like grid, two-terminal component, rotation, port dots, wire between two coordinates.

**Code shown:** `component.ports()`, `rotate_right()`, `create_wire()`.

**Narration:**

> Posicionar um símbolo não basta. O script consulta as portas reais de cada componente e identifica quais são elétricas. Para dispositivos de dois terminais ele verifica a orientação e, se necessário, gira o componente. Só depois utiliza as coordenadas das portas para criar o fio. Essa lógica torna a montagem muito mais robusta.

**Duration:** 32 s.

---

## Scene 09 — SourceCreationScene

**Objective:** Create and parameterize the three-phase source.

**Visuals:** Source symbol, three phase waveforms, parameter list.

**Code shown:** `master:source3`, `MVA`, `Vbase`, `Vm`, `F`, `Ph`.

**Narration:**

> A fonte é uma instância de `master:source3`. O script configura 480 volts linha a linha RMS, 60 hertz e base de 1 MVA. As três tensões são conceitualmente defasadas de 120 graus, formando a alimentação trifásica da ponte retificadora.

**Duration:** 25 s.

---

## Scene 10 — RectifierConstructionScene

**Objective:** Build D1–D6 exactly as in the script.

**Visuals:** Six positions appear; diodes are instantiated one by one; DC buses and phase nodes are connected.

**Code shown:** six `create_diode()` calls.

**Narration:**

> A ponte utiliza a definição `master:peswitch`, mas cada instância é configurada com `Type="DIODE"`. O código cria primeiro D1, D3 e D5 na linha superior e depois D2, D4 e D6 na inferior. Em seguida consulta as portas `DN` e `DP` e constrói os barramentos positivo, negativo e os três nós de fase.

**Duration:** 32 s.

---

## Scene 11 — RectifierOperationScene

**Objective:** Explain electrical six-pulse operation.

**Visuals:** Current path highlighted through one upper and one lower diode; six-pulse DC waveform.

**Code shown:** none.

**Equation:** qualitative six-pulse behavior.

**Narration:**

> Eletricamente, em cada instante uma fase fornece corrente através de um diodo superior e outra fase fecha o caminho por um diodo inferior. A combinação condutora muda a cada 60 graus elétricos. Por isso a tensão retificada apresenta seis pulsos por ciclo fundamental.

**Duration:** 28 s.

---

## Scene 12 — DCFilterScene

**Objective:** Explain the exact DC load arrangement and filtering effect.

**Visuals:** Parallel C/R branches; unfiltered waveform transforms into smoother DC.

**Code shown:** `FILTER_CAPACITANCE_UF = 2200`, `LOAD_RESISTANCE_OHM = 10`.

**Narration:**

> O lado DC possui dois ramos em paralelo. À esquerda, o capacitor `C_FILTER` de 2200 microfarads. À direita, o medidor `Idc` e o resistor `R_LOAD` de 10 ohms. O capacitor reduz a ondulação da tensão DC, mas também torna a corrente absorvida da rede mais pulsante, o que explica a presença de harmônicos.

**Duration:** 30 s.

---

## Scene 13 — MeasurementsAndChannelsScene

**Objective:** Show signal path from meters to output data.

**Visuals:** Ia/Ib/Ic/Idc meters; Meter → Data Label → Output Channel → OUT/INF → CSV.

**Code shown:** `UseSignalName="YES"`, `Scale=1000`, `Units="A"`.

**Narration:**

> O script mede `Ia`, `Ib`, `Ic` e `Idc`. O sinal é associado a um Data Label e depois a um Output Channel. Quando os parâmetros existem, o código ativa o uso do nome do sinal, aplica escala de mil para converter de kA para A e define a unidade de engenharia como ampère.

**Duration:** 29 s.

---

## Scene 14 — SimulationSettingsScene

**Objective:** Distinguish simulation duration, integration step, and channel sample step.

**Visuals:** Code left; 0–0.60 s timeline right.

**Narration:**

> A simulação dura 0,60 segundo. O passo de solução é de 50 microssegundos e o passo de plotagem dos canais também é de 50 microssegundos. A duração total precisa ser suficiente para que o transitório inicial de carregamento do capacitor diminua antes da janela usada na FFT.

**Duration:** 26 s.

---

## Scene 15 — ExecutionScene

**Objective:** Emphasize `project.run()` and EMTDC responsibility.

**Visuals:** Python → PSCAD → EMTDC; progress bar.

**Code shown:** `project.run()`.

**Narration:**

> Aqui acontece a separação mais importante do exemplo. O Python envia a ordem `project.run()`, mas quem integra as equações e resolve a rede no domínio do tempo é o PSCAD com o EMTDC. O script apenas acompanha o processo e verifica as mensagens de erro do projeto.

**Duration:** 23 s.

---

## Scene 16 — WaveformsScene

**Objective:** Introduce distorted phase current and selection of Ia.

**Visuals:** Three conceptual distorted phase currents; Ib/Ic fade and Ia remains.

**Narration:**

> Depois da simulação, as correntes de fase não são perfeitamente senoidais. Nesta animação usamos uma forma de onda sintética apenas para ilustrar o fenômeno, porque o repositório público não contém os resultados numéricos da execução PSCAD. A análise FFT do código utiliza especificamente a corrente da fase A.

**Duration:** 25 s.

---

## Scene 17 — OutputReadingScene

**Objective:** Explain INF/OUT discovery and CSV conversion.

**Visuals:** `.inf` and `.out` → `OutFile` → CSV → NumPy arrays.

**Code shown:** `OutFile`, `.open()`, `.columns()`, `.close()`, `.toCSV()`.

**Narration:**

> O script procura os arquivos `INF` na pasta temporária do projeto e seleciona o conjunto de resultados correspondente. O `OutFile` é aberto apenas para inspecionar as colunas e depois fechado. Isso é importante porque `toCSV()` abre o arquivo internamente; fechar antes evita o erro `Already open`. Depois o CSV é lido e convertido em arrays NumPy de tempo e corrente.

**Duration:** 32 s.

---

## Scene 18 — FFTWindowScene

**Objective:** Explain final 12-cycle selection.

**Visuals:** Full 0.60 s current; final 0.20 s highlighted.

**Equations:** `T1 = 1/60 = 16.67 ms`; `TFFT = 12 T1 = 0.20 s`.

**Narration:**

> Em 60 hertz, um ciclo dura aproximadamente 16,67 milissegundos. Como o código usa os últimos 12 ciclos, a janela de análise tem aproximadamente 0,20 segundo. Assim, em uma simulação de 0,60 segundo, a FFT tende a usar a parte final, depois do maior transitório de inicialização.

**Duration:** 28 s.

---

## Scene 19 — FFTScene

**Objective:** Explain time-to-frequency transformation.

**Visuals:** Distorted Ia(t) transforms into spectral lines.

**Narration:**

> A DFT é a transformação matemática que representa o sinal como componentes de frequência. A FFT é o algoritmo eficiente usado para calcular essa DFT. Como a corrente no tempo é real, o código utiliza `rfft`, que retorna apenas o espectro de frequências não negativas.

**Duration:** 26 s.

---

## Scene 20 — HarmonicsScene

**Objective:** Explain integer harmonic extraction and six-pulse characteristic orders.

**Equations:** `fh = h f1`; `h = 6k ± 1`.

**Narration:**

> Para cada ordem de 1 a 25, o script calcula a frequência alvo `h` vezes 60 hertz e escolhe o bin da FFT mais próximo. Em um conversor ideal de seis pulsos, as correntes características seguem a família `6k ± 1`, como quinta e sétima, décima primeira e décima terceira. Essa relação é uma referência teórica; o espectro real depende do circuito e do regime de operação.

**Duration:** 31 s.

---

## Scene 21 — THDScene

**Objective:** Build the exact THD definition used by the code.

**Equation:** `THD_I = sqrt(sum_{h=2}^{25}(I_h/I_1)^2) × 100%`.

**Narration:**

> A fundamental, `I1`, funciona como referência. O código pega as componentes da segunda até a vigésima quinta ordem, divide cada uma pela fundamental, eleva ao quadrado, soma, tira a raiz quadrada e converte para porcentagem. Essa é exatamente a faixa de ordens utilizada pela implementação atual.

**Duration:** 27 s.

---

## Scene 22 — ResultsScene

**Objective:** Show all generated artifacts.

**Visuals:** Project folder with `.pswx`, `.pscx`, current CSV, FFT image, harmonic image, harmonic CSV, summary text.

**Narration:**

> Ao final, o processo deixa tanto os arquivos do modelo PSCAD quanto os resultados de pós-processamento. O CSV contém os canais no domínio do tempo. As duas figuras mostram o espectro contínuo e o espectro por ordem harmônica. O arquivo de resumo registra a fundamental e o THD.

**Duration:** 26 s.

---

## Scene 23 — FullWorkflowScene

**Objective:** Give the strongest synchronized mental model of program execution.

**Visuals:** Three columns: Python code, PSCAD visual state, progress/checkmark.

**Narration:**

> Agora podemos enxergar o script como se estivesse executando. `create_source` cria a fonte. `create_bridge` monta a ponte. `create_dc_load` fecha o lado DC. Os canais são criados, o PSCAD executa a simulação e os resultados retornam ao Python para a FFT. Esta é a cena que une programação, circuito e fluxo de trabalho.

**Duration:** 34 s.

---

## Scene 24 — GeneralizationScene

**Objective:** Show reuse beyond the rectifier example.

**Visuals:** PSCAD + Python center with radial study categories.

**Narration:**

> O maior valor do exemplo não é o retificador em si. O mesmo padrão pode automatizar filtros harmônicos, energização de transformadores, inrush, chaveamentos de capacitores, curtos-circuitos, TRV, linhas, cabos, máquinas síncronas e varreduras paramétricas. Mudam o modelo e os resultados; a arquitetura de automação permanece semelhante.

**Duration:** 27 s.

---

## Scene 25 — PortabilityScene

**Objective:** Explain what must change on another computer.

**Visuals:** Machine-specific path transforms into `SCRIPT_DIR` portable path; environment checks.

**Narration:**

> O arquivo Python atual ainda contém um caminho absoluto específico da máquina onde foi desenvolvido. O README recomenda usar a pasta do próprio script como referência, tornando o repositório portátil. Também é preciso conferir a versão do PSCAD, arquitetura x64, disponibilidade de `mhi.pscad` no Python e uma licença que permita a Automation Library.

**Duration:** 31 s.

---

## Scene 26 — ConclusionScene

**Objective:** Close with the complete engineering message.

**Visuals:** Python Code → Automatic PSCAD Model → EMT Simulation → Engineering Results.

**Narration:**

> O exemplo mostra uma cadeia completa de engenharia automatizada. O Python cria e configura o modelo, o PSCAD executa a simulação de transitórios eletromagnéticos e o Python volta a assumir o controle para transformar sinais em resultados de engenharia. Esse padrão é a base para uma biblioteca crescente de estudos PSCAD reproduzíveis e automatizados.

**Duration:** 20 s.

---

# Narration recording notes

- Speak function and class names more slowly than normal prose.
- Preserve API names in English: `workspace`, `case`, `canvas`, `Output Channel`, `OutFile`, `rFFT`.
- When saying quantities, use engineering pronunciation: “quatrocentos e oitenta volts linha a linha RMS”, “cinquenta microssegundos”, “dois mil e duzentos microfarads”.
- Do not narrate every visible line of code. The visual shows syntax; narration should explain engineering meaning.
- Pause briefly before the three conceptual boundaries: Python automation, PSCAD numerical solution, Python post-processing.


Revision 2026-09-07: visual corrections follow docs/CHANGE_PLAN.md. FullWorkflowScene uses compact icons; PortabilityScene stacks the code examples; ConclusionScene uses a two-line title. The original narration remains Portuguese as a separate aid and is not embedded in the silent MP4.
