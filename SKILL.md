---
name: simplified-technical-portuguese
description: "Use quando um texto em português precisa ser interpretado sem um humano para resolver ambiguidades (descrições de ferramentas, mensagens de erro, instruções entre agentes, prompts de sistema, relatórios de status) e uma leitura errada tem custo real, ou quando o texto está denso, cheio de ressalvas ou fácil de interpretar mal. Gatilhos: desambiguar, português técnico simplificado, linguagem simples, aplicar o STE100 em português, reescrever para que um agente não interprete errado, tirar o traduzês. Não serve para textos criativos ou de marketing."
version: 0.1.0
---

# Português Técnico Simplificado

O ASD-STE100 (Simplified Technical English, ou STE) é uma norma de linguagem controlada criada pela indústria aeroespacial e de defesa. A ASD (AeroSpace and Defence Industries Association of Europe) mantém a norma. O objetivo dela é impedir que técnicos de manutenção interpretem errado instruções em inglês. A norma remove as duas maiores fontes de erro de leitura: palavras com mais de um significado e frases com mais de uma estrutura possível.

O STE existe só em inglês, e não há norma equivalente para o português. Esta skill leva a mesma disciplina para o português do Brasil e para outro leitor: um **agente de IA ou um sistema**. Esse leitor precisa interpretar um texto sem um humano para resolver ambiguidades. Esse texto pode ser uma mensagem de erro, a descrição de uma ferramenta, uma instrução entre agentes ou um relatório de status. Um técnico pode ler "o job deve terminar em cinco minutos" como ordem ("precisa terminar") ou como estimativa ("provavelmente termina"). Um modelo de linguagem também pode.

## Quando usar esta skill

- A saída de um agente (explicação, instrução, mensagem de log, descrição de ferramenta) está densa, cheia de jargão ou ambígua.
- Outro agente, um pipeline de tradução ou um leitor leigo vai consumir o texto. Uma leitura errada tem custo real.
- Você está escrevendo um prompt, uma mensagem de sistema ou a descrição de uma ferramenta. Você quer remover a ambiguidade antes que um modelo leia o texto.
- Um modelo gerou o texto em português, e o texto tem "traduzês": decalques do inglês, gerundismo, "o mesmo" no lugar de pronome, "seu" em excesso.
- Você quer uma comparação **antes e depois** que mostre qual regra o texto violou e como a reescrita corrige o problema. Peça explicitamente. A saída padrão é só o texto reescrito (veja Formato da saída).

Esta skill não serve para textos criativos ou de marketing. O estilo do STE é plano e literal de propósito. Não aplique a skill a um texto em que a voz, a nuance ou a persuasão são o objetivo.

## Dois modos

Escolha um modo antes de reescrever. Se o usuário não disser qual, deduza pelo tipo de texto e informe a escolha numa linha.

**Estrito**: procedimentos, mensagens de erro, descrições de ferramentas e funções, instruções entre agentes, textos de segurança. Vale para todo lugar onde uma leitura errada tem custo. Aplique todas as regras abaixo, inclusive os limites de palavras e a disciplina de uma palavra para um significado.

**Flexível**: READMEs, descrições de pull request, changelogs, prosa explicativa. Aplique as regras estruturais por inteiro e trate as regras lexicais como recomendação (veja a divisão em Regras centrais). Na prática, você mantém os limites de palavras, a voz ativa e os tempos simples. Você também mantém a proibição de ponto e vírgula, verbo-suporte, locuções prolixas e adjetivos de marketing. Você abandona o vocabulário fixo. A prosa precisa de alguma variedade, e uma reescrita estrita de prosa parece um transplante de personalidade, não um esclarecimento.

Os dois modos e a divisão entre regras estruturais e lexicais são a mesma distinção vista de dois lados. A divisão diz quais regras esta skill consegue verificar sem um dicionário. Os modos dizem quais delas impor em cada tipo de texto.

## Fontes e escopo

Esta skill segue as **categorias de regras** do ASD-STE100 Issue 9 (janeiro de 2025). A norma tem 53 regras de redação em 9 seções: escolha de palavras, gramática, estrutura da frase e estilo. A norma tem também um dicionário de cerca de 900 palavras aprovadas, cada uma com um significado e uma classe gramatical. O dicionário lista ainda cerca de 1.200 palavras a evitar, com substitutas sugeridas. O resumo completo e as citações estão em `references/regras-de-redacao.md`.

A skill **não** reproduz o dicionário do ASD. O ASD-STE100 é gratuito, mas a redistribuição não é livre. O Issue 9 (página 2) proíbe a reprodução sem autorização escrita de um diretor do ASD. A norma libera a reprodução só para oito categorias de organizações. Este projeto não está em nenhuma delas. Além disso, o dicionário é de palavras inglesas e não se aplica ao português.

Não existe linguagem controlada oficial para o português. As referências brasileiras mais próximas são de linguagem simples:

- A **Lei nº 15.263/2025** (Política Nacional de Linguagem Simples). O Art. 5º lista técnicas que coincidem com regras do STE. Entre elas estão a ordem direta, as frases curtas, uma ideia por parágrafo, as palavras comuns e a voz ativa. A lei manda também evitar frases intercaladas, substantivos no lugar de verbos e palavras estrangeiras que não sejam de uso corrente.
- A **ABNT NBR ISO 24495-1:2024**, versão brasileira da norma internacional de linguagem simples.

Por isso, esta skill aplica o *princípio* do STE: a palavra mais simples e comum, usada sempre do mesmo jeito. Ela também adapta as regras estruturais à gramática do português. Ela acrescenta regras para fontes de ambiguidade que o inglês não tem, como o "dever" ambíguo, o "seu" com dois donos e o sujeito oculto. A ortografia segue o Acordo Ortográfico de 1990 e o VOLP da Academia Brasileira de Letras.

## Regras centrais

As regras do STE são de dois tipos, e esta skill só consegue cumprir um deles por inteiro. As **regras estruturais** são autossuficientes: elas descrevem a forma da frase, e você consegue aplicá-las só pela descrição. As **regras lexicais** dependem por inteiro de um dicionário aprovado. O dicionário do ASD é em inglês, e não existe um equivalente em português. Sem dicionário, as regras lexicais deixam de ser uma norma verificável e viram uma preferência por palavras simples.

Aplique as regras estruturais com confiança. Aplique as regras lexicais como uma direção. Diga isso na sua saída e não sugira uma conformidade com dicionário que você não pode verificar.

### Regras estruturais: aplique

| Regra | Faça | Não faça |
|---|---|---|
| Voz ativa | "O agente exclui o arquivo." | "O arquivo é excluído pelo agente." ou "Exclui-se o arquivo." A partícula "se" também esconde quem age. Use a voz passiva só quando quem age é desconhecido ou irrelevante. |
| Verbo pleno, sem verbo-suporte (Regra 3.7) | "Analise o log." / "Remova o painel." | "Realize uma análise do log." / "Proceda à remoção do painel." O substantivo de ação alonga a frase e esconde quem age. |
| Sem locuções prolixas (no lugar da Regra 9.3) | "para", "porque", "sobre", "está" | "a fim de", "tendo em vista que", "no que diz respeito a", "encontra-se", "sendo que". O português não tem phrasal verbs, então a Regra 9.3 não se aplica. O vício mais próximo é a locução de várias palavras no lugar de uma palavra simples. |
| Uma instrução por frase | "Abra o arquivo. Leia a linha 3." | "Abra o arquivo e leia a linha 3, depois confira se ela corresponde." |
| Tamanho da frase | Até 20 palavras em instruções e procedimentos, até 25 em descrições | Frases longas com orações coordenadas e subordinadas em cadeia |
| Sem ponto e vírgula (Regra 8.1) | Divida em frases separadas. | Qualquer ponto e vírgula, inclusive no fim de itens de lista no estilo jurídico ("I - ...; II - ...; e"). A Regra 8.1 permite todos os outros sinais. O travessão não é proibido, mas costuma indicar uma frase que deveria ser dividida. |
| Ordem direta, sem intercaladas | "O servidor rejeita a requisição se o token expirou." | "O servidor, caso o token, emitido pelo serviço de autenticação, tenha expirado, rejeita a requisição." |
| Cadeias de "de" | No máximo três "de" seguidos num grupo nominal ("o arquivo de configuração do servidor de testes") | "a válvula de entrada do conjunto da bomba de combustível de alta pressão". O grupo nominal empilhado do inglês vira uma cadeia de "de" em português. |
| Sujeito explícito quando ele muda | "O cliente envia o pedido. O servidor valida o pedido." | "O cliente envia o pedido. Valida o pedido." O português permite sujeito oculto. Quando o sujeito muda, o leitor não sabe quem age. |
| Sem elipse | "Os pedidos sem nota fiscal foram cancelados." | "Pedidos sem nota cancelados." O estilo telegráfico apaga o verbo, e o leitor não sabe se a frase é um relato ou uma ordem. |
| Referência sem ambiguidade | "O agente enviou ao usuário o token do usuário." / "Antes de excluir o arquivo, copie o arquivo." | "O agente enviou ao usuário seu token." (de quem?) / "Antes de excluir o arquivo, copie o mesmo." ("o mesmo" no lugar de pronome) |
| Preserve a modalidade | "A requisição **pode ter** falhado." continua "pode ter falhado". | Promover uma ressalva a fato ("A requisição falhou.") ou inventar uma certeza que a fonte não deu. Em português, "deve" é ambíguo: ordem ou estimativa. Se a fonte é ambígua, não escolha em silêncio. |
| Tratamento uniforme | "Você" e imperativo em todo o documento: "Remova", "Clique", "Verifique" | Misturar "Remova" (você) com "Remove" ou "Clica" (tu), ou com instruções no infinitivo ("Remover o painel"), no mesmo documento |
| Siglas | O nome por extenso na primeira ocorrência: "tempo de vida (TTL)" | Uma sigla que o texto nunca define |
| Limites de parágrafo | Um tópico por parágrafo, até 6 frases | Parágrafos com vários tópicos |
| Listas para sequências | Uma lista numerada ou com marcadores para 3 ou mais passos ou condições | Uma sequência escondida numa frase só |

### Regras lexicais: só direção

| Regra | Faça | Não faça | Por que a regra é mais fraca aqui |
|---|---|---|---|
| Uma palavra, um significado | Escolha um verbo para uma ação e use-o sempre. Por exemplo, sempre "verifique", sem alternar "verifique", "confira", "cheque" e "valide" para a mesma ação. | Alternar sinônimos para a mesma ideia ao longo do documento | A consistência dentro do documento é verificável. Qual palavra é a *aprovada* não é, porque não existe dicionário aprovado para o português. |
| Uma classe gramatical por palavra | "Grave o evento no log." (log = substantivo) | "Logue o evento." (log virou verbo) | Sem dicionário, não há lista das palavras que são só substantivo. Prefira a forma substantiva quando as duas se leem bem. Não declare conformidade. |
| Termos de domínio | Mantenha os termos técnicos necessários e defina cada um uma vez se ele não for comum. O STE permite um glossário próprio do projeto além do dicionário-base. | Jargão que o texto nunca define | A permissão de glossário existe no STE, mas o dicionário-base que ela estende não existe em português. |
| Estrangeirismos e falsos cognatos | Use a palavra portuguesa consolidada: "excluir", "definir", "desempenho", "obrigatório". Mantenha empréstimos técnicos consolidados (commit, deploy, log, backup) e defina-os se o leitor puder não conhecê-los. | "Deletar", "setar", "performance", "mandatório". Falsos cognatos: "eventualmente" (= às vezes, não "por fim"), "assumir que" (= supor), "endereçar o problema" (= tratar), "suportar JSON" (= aceitar). | O limite entre empréstimo consolidado e anglicismo evitável varia por equipe. A Lei 15.263 manda evitar palavras estrangeiras "que não sejam de uso corrente", mas não lista quais são. |

### Tempos verbais: aplique com exceções

O STE permite infinitivo, imperativo, presente simples, passado simples, futuro simples e particípio passado usado como adjetivo. A norma exclui o present perfect e as outras formas compostas.

Em português, a regra muda em quatro pontos:

1. **O pretérito perfeito simples já cobre o present perfect do inglês.** "The job has completed" é "O job terminou" (ou "já terminou"). Não traduza por "O job tem terminado". Em português, "tem" + particípio indica repetição ou continuidade até agora: "o build tem falhado desde segunda" quer dizer que ele falhou várias vezes. Use o tempo composto só quando a repetição é o ponto, e sinalize.
2. **O subjuntivo é obrigatório em condições e finalidades.** Escreva "se o arquivo existir" e "para que o job termine". Prefira "se" + futuro do subjuntivo para condições. Em instruções, evite hipóteses no imperfeito do subjuntivo ("se o arquivo existisse").
3. **Futuro.** Descreva o comportamento de um sistema no presente: "A ferramenta exclui o arquivo." Quando o tempo importa, use o futuro simples ("excluirá") ou "vai" + infinitivo ("vai excluir"), com uma só forma no documento. Nunca use gerundismo ("vamos estar enviando").
4. **Gerúndio.** Use o gerúndio só para ações simultâneas. Considere "O agente lê o arquivo, gerando um relatório". A oração com gerúndio não diz se a segunda ação é simultânea, posterior ou consequência da primeira. Escreva duas frases.

Evite também o mais-que-perfeito simples ("falhara"), que soa arcaico, e a mesóclise ("far-se-á"). Use o mais-que-perfeito composto ("tinha falhado") só quando a ordem dos eventos importa.

**A modalidade é a exceção.** As formas compostas com verbo modal carregam a ressalva. Exemplos: "pode ter falhado", "deve ter travado", "talvez tenha falhado" e "teria falhado". No jornalismo, "teria falhado" quer dizer "supostamente falhou". Mantenha essas formas. Quando a regra dos tempos e a regra da modalidade entram em conflito, a modalidade vence.

## Lista de varredura

Os oito hábitos abaixo explicam a maior parte da dificuldade de ler um texto em português gerado por máquina. Cada um é mecânico: você aponta a palavra ou o sinal exato que quebra a regra, sem julgamento. Procure os oito antes de reescrever.

1. **Rotação de sinônimos**: a mesma coisa recebe vários nomes no mesmo documento ("o usuário", "o cliente", "o consumidor"). O leitor não sabe se é uma coisa ou três. Correção: escolha um nome e use-o sempre.
2. **Empilhamento de ressalvas**: verbos auxiliares e qualificadores se acumulam até a frase não afirmar nada ("vale ressaltar que isso pode potencialmente ajudar a melhorar"). Correção: afirme o fato ou corte a frase.
3. **Verbo-suporte**: uma ação congelada num substantivo ("realizar a análise de", "efetuar o pagamento", "proceder à remoção", "fazer uso de"). Correção: use o verbo ("analisar", "pagar", "remover", "usar").
4. **Adjetivos de marketing**: palavras que afirmam qualidade em vez de mostrá-la. Por exemplo: robusto, poderoso, inovador, intuitivo, de ponta, revolucionário, sem esforço. Correção: corte, ou troque pela medida que justifica a afirmação.
5. **Frases encadeadas**: várias ideias ligadas por ponto e vírgula, travessão, "sendo que" ou gerúndio depois de vírgula. Correção: uma ideia por frase.
6. **Gerundismo**: "vou estar enviando", "vamos estar verificando". Correção: "vou enviar", "verificaremos".
7. **Decalques do inglês**: construções copiadas do inglês. Exemplos: "eventualmente" no sentido de "por fim", "assumir que", "endereçar o problema", "suportar o formato" e "alavancar". Outros: "uma vez que" no sentido de "depois que" e o "seu" em excesso ("Abra seu navegador" em vez de "Abra o navegador"). Modelos treinados sobretudo em inglês produzem esse traduzês com frequência. Correção: use a construção do português.
8. **Referência solta**: "o mesmo" ou "a mesma" no lugar de um nome, "seu" ou "sua" com dois donos possíveis, um pronome longe do nome. Correção: repita o nome.

## Processo

1. Escolha o modo (Estrito ou Flexível). Informe o modo só quando o usuário pedir a tabela de regras (veja Formato da saída).
2. Leia o texto uma vez pelo sentido. Não comece a reescrever antes de entender o que o texto ainda precisa dizer depois.
3. Percorra o texto frase por frase. Marque cada violação das tabelas de Regras centrais e cada hábito da Lista de varredura. No modo Flexível, marque as regras lexicais, mas não as imponha. Para uma primeira passada mecânica nas regras estruturais, rode `scripts/pts-lint.py` (veja Linter abaixo).
4. Reescreva cada frase marcada. Corrija a violação e preserve o sentido original com exatidão. Se a reescrita perder uma precisão necessária (uma condição de segurança, um limite de escopo, um número), mantenha a forma longa e sinalize. Não simplifique em silêncio.
   - **Verifique a modalidade antes de fechar a reescrita.** Ressalvas ("pode", "poderia", "às vezes", "é provável que") carregam o grau de certeza do autor, e o grau de certeza é conteúdo. Uma frase mais curta que promove uma ressalva a fato não é uma simplificação. É outra afirmação. Esse é o erro mais comum numa reescrita bem-intencionada, porque as ressalvas são justamente o que o limite de palavras convida a cortar.
   - **Não resolva sozinho a ambiguidade de "dever".** Se a fonte diz "o job deve terminar em cinco minutos" e o contexto não diz se é ordem ou estimativa, não escolha. Mantenha a frase e sinalize na linha `Mantido como está:`.
   - Nunca acrescente um fato que a fonte não afirmou. Uma reescrita que fica melhor porque fornece uma causa, uma frequência ou um mecanismo deixou de ser uma reescrita.
5. Entregue o texto reescrito (veja Formato da saída). Guarde para você a escolha de modo e a análise das regras, a menos que o usuário peça para vê-las.
6. Se o texto já está conforme, diga isso. Não force mudanças num texto conforme.

### Linter

`scripts/pts-lint.py` usa só a biblioteca padrão do Python. Ele lê stdin ou arquivos e, com `--json`, produz saída estruturada.

- **Achados obrigatórios** reprovam a execução. São eles: ponto e vírgula, frase longa, locução prolixa, verbo-suporte, adjetivo de marketing e gerundismo. Também são obrigatórias a rotação de sinônimos (com as conjugações dos verbos) e a conjunção pendente no fim de item de lista.
- **Achados consultivos** nunca reprovam a execução. São eles: voz passiva, partícula "se", tempo composto, cadeia de "de", "o mesmo", gerúndio depois de vírgula, decalque do inglês e travessão.
- O linter **nunca** marca ressalvas nem modalidade. O `--autoteste` comprova que "pode ter falhado", "talvez tenha falhado" e "teria falhado" passam limpos.

O linter lê Markdown por parágrafo, então uma frase quebrada em várias linhas conta como uma frase. Num arquivo `.rs`, ele lê só a prosa: comentários de documentação e comentários. Com `--partes mensagens`, ele lê também as strings de `panic!`, `expect`, `assert!` e chamadas parecidas, com o limite estrito de 20 palavras.

Opções: `--linha-de-base N` tolera N violações obrigatórias (para adotar o linter em documentos existentes). `--desativar regra1,regra2` silencia regras, `--max-palavras N` define o limite de palavras e `--resumo` ordena vários arquivos pelo número de violações. `--ajuda` mostra o uso completo.

O linter não verifica a ordem direta, o sujeito oculto, o "seu" ambíguo, o "dever" ambíguo nem o tratamento misto (tu e você). Essas regras precisam de leitura humana ou de um modelo.

## Formato da saída

**Padrão: o texto reescrito, e nada mais.** Quem chama a skill quase sempre quer um resultado para colar direto numa descrição de ferramenta, numa string de erro ou num prompt. Mostre só o texto simplificado. Não acrescente preâmbulo sobre esta skill, anúncio de modo, contagem de violações, resumo das mudanças, tabela de regras nem oferta final de explicação.

O único acréscimo permitido: se o passo 4 manteve uma forma longa de propósito, acrescente uma linha depois do texto com o prefixo `Mantido como está:`. A linha nomeia o trecho e a precisão que se perderia. Omita a linha quando não houver nada a informar.

**Sob pedido: a tabela de regras.** O usuário pode pedir para ver o raciocínio: "mostre o diff", "quais regras ele quebrou", "explique as mudanças", "antes e depois". Nesse caso, entregue esta tabela no lugar do texto:

```markdown
| Regra violada | Original | Simplificado |
|---|---|---|
| Tempo composto (decalque do present perfect) | "Temos recebido a sua solicitação." | "Recebemos a sua solicitação." |
| Cadeia de "de" (4 ou mais) | "o módulo de controle de prioridade da fila de tarefas do agente" | "o módulo que controla a prioridade da fila de tarefas do agente" |

Modo: Estrito. 7 violações encontradas.
```

Depois da tabela, escreva uma linha sobre o que você **não** simplificou de propósito, e por quê. Em geral, a simplificação perderia uma precisão necessária.

## Documentação num repositório de código

Quando o texto está num repositório (comentários, docstrings, READMEs, textos de ajuda), edite os arquivos no lugar. Não imprima o texto. Aplique também estas regras:

- **Modo pelo tipo de texto.** Comentários, docstrings e documentos Markdown usam o modo Flexível. Mensagens de erro, de panic e de log usam o modo Estrito. O texto de ajuda da linha de comando também usa o modo Estrito.
- **Mexa só na prosa.** Não mude código, identificadores, trechos de código, destinos de links nem textos de títulos (os títulos são âncoras de links). Mantenha a largura de linha do arquivo. Identificadores e nomes de opções em inglês continuam em inglês.
- **Procure nos testes antes de mudar uma mensagem.** Os testes muitas vezes comparam parte de uma string de erro (`should_panic(expected = …)`, `assert!(msg.contains(…))`, arquivos de snapshot). Mantenha cada trecho comparado.
- **Atualize todas as cópias.** Um texto de ajuda ou um parágrafo de documentação pode ter uma cópia idêntica em outro arquivo. Mude todas as cópias juntas.
- **Documentação contra código.** Quando um comentário e o código discordam, não ajuste a prosa a nenhum dos lados em silêncio. Mostre a evidência (a linha de código, um teste, um programa pequeno) e pergunte qual lado é a intenção.
- **Descreva o estado atual.** A documentação diz o que o código faz agora, não como ele mudou. `--ativar historico` marca frases de changelog ("não mais", "anteriormente", "atualmente").
- **Compile e teste depois.** Rode a geração da documentação e os testes. Um comentário de documentação movido pode mudar a resolução dos links dele.

## Limites

**A skill faz:**
- Reescreve um português ambíguo ou denso em frases curtas, de significado único e na voz ativa.
- Devolve só o texto reescrito por padrão, e nomeia as regras aplicadas quando o usuário pede.
- Preserva cada fato, condição e limite de escopo do original.
- Preserva a força de cada ressalva e não acrescenta afirmações que a fonte não fez.
- Sugere uma entrada de glossário de uma linha para os termos de domínio que precisam ficar.

**A skill não faz:**
- Reproduzir o dicionário oficial de cerca de 900 palavras do ASD como se o tivesse memorizado. Para a redação aprovada em inglês, o download oficial é sempre a fonte de verdade.
- Simplificar textos criativos, de marketing ou persuasivos, em que a voz e a nuance são o objetivo.
- Cortar em silêncio uma condição de segurança, uma exceção ou um limite de escopo para encurtar uma frase. Ela sinaliza a troca.
- Converter "pode ter falhado" em "falhou", ou "pode ser causado por X" em "X é a causa". Perder uma ressalva muda a afirmação.
- Escolher em silêncio entre os dois sentidos de "dever" (ordem ou estimativa).
- Garantir um documento conforme ao STE. O STE é uma norma em inglês, e esta skill é uma ferramenta geral de clareza inspirada nele, não uma ferramenta certificada. Ela também não garante conformidade com a Lei 15.263 ou com a ABNT NBR ISO 24495-1. Essas normas tratam de muito mais que redação: teste com o público, acessibilidade, leiaute.
- Revisar ortografia e gramática como objetivo principal. A skill trata de ambiguidade.
- Tornar verdadeiro ou útil um conteúdo fraco. O STE corrige a *forma* de um texto, não a substância. Um parágrafo vazio reescrito com estas regras vira um parágrafo vazio limpo, curto e bem pontuado. Se o texto não tem nada a dizer, nenhuma reescrita resolve isso. Diga isso em vez de polir o texto.
- Encurtar além do ponto da clareza. O objetivo não é cortar palavras, é remover a ambiguidade. A partir de certo ponto, a compressão começa a custar tempo ao leitor em vez de economizar. Pare quando a frase não tiver ambiguidade, não quando ela for a mais curta possível.

## Recursos adicionais

- **`references/regras-de-redacao.md`**: resumo das regras e do dicionário do STE, e a adaptação de cada regra ao português. Inclui as citações da norma oficial, da legislação brasileira e de fontes secundárias.
- **`examples/antes-depois.md`**: exemplos comentados. Inclui ilustrações das regras do STE, regras próprias do português e exemplos de saída de agentes criados para esta skill.
- **`scripts/pts-lint.py`**: linter determinístico das regras estruturais (veja Linter acima). Ele sai com código 1 quando as violações obrigatórias passam de `--linha-de-base` (padrão 0). `--ativar historico` acrescenta a regra opcional de histórico. Um nome de regra desconhecido é erro (código 2).
