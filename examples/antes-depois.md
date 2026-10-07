# Exemplos de antes e depois

## Parte 1: regras do STE, adaptadas ao português

Estes exemplos ilustram regras reais do ASD-STE100, a partir de fontes secundárias públicas (veja `references/regras-de-redacao.md`). São paráfrases adaptadas ao português, não citações da norma. A norma oficial dá exemplos só em inglês.

| Regra | Antes | Depois | Por quê |
|---|---|---|---|
| Um significado por palavra | "Verifique o sistema." / "Confira as conexões." / "Valide o recebimento." | "Verifique o sistema." / "Verifique as conexões." / "Verifique o recebimento." (um só termo, usado de forma consistente) | Três quase sinônimos obrigam o leitor a adivinhar se eles nomeiam a mesma ação. |
| Uma classe gramatical por palavra | "Logue o evento." | "Grave o evento no log." | Se "log" é aprovado só como substantivo, usar a palavra como verbo quebra a garantia de uma palavra para uma função. |
| Significado preciso do verbo | "Siga as instruções de segurança." | "Obedeça às instruções de segurança." | "Seguir" pode querer dizer "obedecer" ou "ir para" ("siga para a próxima etapa"). O STE escolhe a palavra sem ambiguidade. |
| Só tempos simples | "Temos recebido o relatório técnico da matriz." | "Recebemos o relatório técnico da matriz." | Em português, "temos recebido" indica repetição ("recebemos várias vezes"). Com um relatório só, a frase é um decalque do present perfect, e o pretérito perfeito diz o fato. |
| Verbo, não substantivo | "Realize uma inspeção do filtro." | "Inspecione o filtro." | O substantivo esconde a ação e acrescenta um verbo vazio. |
| Sem locuções prolixas (no lugar dos phrasal verbs) | "A fim de liberar espaço, proceda à remoção dos logs antigos." | "Para liberar espaço, remova os logs antigos." | O português não tem phrasal verbs. O vício equivalente é a locução de várias palavras ("a fim de", "proceda à remoção") no lugar de uma palavra simples ("para", "remova"). |

## Parte 2: regras próprias do português

Estas regras não existem no STE. Elas tratam de fontes de ambiguidade do português e do traduzês que os modelos de linguagem produzem.

| Regra | Antes | Depois | Por quê |
|---|---|---|---|
| Gerundismo | "Vamos estar enviando o relatório amanhã." | "Vamos enviar o relatório amanhã." | "Ir" + "estar" + gerúndio não acrescenta sentido ao futuro e alonga a frase. |
| "O mesmo" como pronome | "Antes de excluir o arquivo, faça uma cópia do mesmo." | "Antes de excluir o arquivo, copie o arquivo." | "O mesmo" no lugar de um nome obriga o leitor a procurar o referente. Repita o nome. A reescrita também troca o verbo-suporte ("faça uma cópia") pelo verbo. |
| "Seu" com dois donos | "O agente enviou ao usuário seu token." | "O agente enviou ao usuário o token do usuário." | "Seu" pode ser do agente, do usuário ou de você. "Dele" também não resolve, porque os dois nomes são masculinos. |
| "Dever" ambíguo | "O job deve terminar em cinco minutos." | Se é ordem: "O job precisa terminar em cinco minutos." Se é estimativa: "O job provavelmente termina em cinco minutos." | Uma frase, duas leituras. Se o contexto não decide, a reescrita também não decide. Ela mantém a frase e sinaliza na linha `Mantido como está:`. |
| Sujeito oculto com troca de sujeito | "O cliente envia o pedido ao servidor, que valida o token. Se o token expirou, rejeita o pedido." | "O cliente envia o pedido ao servidor. O servidor valida o token. Se o token expirou, o servidor rejeita o pedido." | O sujeito oculto de "rejeita" pode ser o cliente (sujeito da frase anterior) ou o servidor. A reescrita nomeia o servidor, porque a fonte diz que o servidor valida o token. |
| Tratamento uniforme | "Abre o painel. Remova o filtro. Limpar a tela." | "Abra o painel. Remova o filtro. Limpe a tela." | "Abre" (tu) é também a forma de "ele abre". O leitor não sabe se a frase é uma ordem ou uma descrição. O infinitivo "Limpar" muda de registro no meio do procedimento. |
| Decalque: "eventualmente" | "O cache é eventualmente invalidado." | Se o sentido é "eventually": "O cache é invalidado mais tarde." Se o sentido é "às vezes": "O cache é invalidado às vezes." | Em português, "eventualmente" quer dizer "às vezes" ou "por acaso". Quem escreve pensando em "eventually" quer dizer "mais cedo ou mais tarde". A voz passiva fica, porque a fonte não diz quem invalida o cache. |
| Decalque: "uma vez que" | "Uma vez que o deploy terminou, o agente libera o tráfego." | Se é tempo: "Depois que o deploy termina, o agente libera o tráfego." Se é causa: "Como o deploy terminou, o agente libera o tráfego." | Com o indicativo, "uma vez que" indica causa ("já que"). Como decalque de "once", indica tempo. |
| Locução prolixa e verbo-suporte | "O servidor encontra-se indisponível. Favor efetuar uma nova tentativa." | "O servidor está indisponível. Tente de novo." | "Encontra-se" é "está" com mais palavras. "Favor efetuar" junta o infinitivo de cortesia ao verbo-suporte. |

## Parte 3: aplicado à saída de agentes

Estes são exemplos originais, criados para o uso real desta skill: reescrever a saída de agentes de IA para que outro agente, uma camada de tradução ou um leitor leigo possa interpretar o texto sem ambiguidade. São ilustrações, não citações de um sistema real.

As contagens de palavras abaixo contam os trechos separados por espaço (`text.split()`), e a pontuação não conta à parte. Outro tokenizador vai produzir outro número.

### Exemplo A: descrição de ferramenta

**Antes:**
> Esta ferramenta irá tentar realizar a sincronização do estado entre os diversos backends que foram configurados, e caso um conflito seja detectado ela poderá resolvê-lo automaticamente dependendo da estratégia que tiver sido definida, ou caso contrário irá apresentar o conflito para revisão manual.

**Violações marcadas:**
- Duas instruções numa frase (sincronizar, e depois resolver ou apresentar o conflito).
- Verbo-suporte ("realizar a sincronização").
- Voz passiva nas orações subordinadas ("foram configurados", "seja detectado", "tiver sido definida").
- 43 palavras, muito acima do limite de 25 para descrições.

Note o que *não* foi marcado: "irá tentar" e "poderá resolvê-lo". São ressalvas, não violações. A ferramenta não promete sucesso, e a reescrita também não pode prometer.

**Depois:**
> A ferramenta tenta sincronizar o estado entre os backends configurados. Se encontrar um conflito, a ferramenta lê a estratégia configurada. Se a estratégia permitir resolução automática, a ferramenta pode resolver o conflito automaticamente. Se a ferramenta não resolver o conflito, ela encaminha o conflito para revisão manual.

A última frase depende de a ferramenta resolver ou não o conflito, e não do que a estratégia permite. Esse é o sentido de "ou caso contrário" no original: o caminho alternativo cobre também uma resolução permitida que não aconteceu.

### Exemplo B: mensagem de erro

**Antes:**
> Um erro pode ter ocorrido durante o processamento da sua requisição devido a uma possível incompatibilidade no formato de dados esperado, o que poderia ser causado por uma versão desatualizada do cliente.

**Violações marcadas:**
- Uma frase com três afirmações separadas (um erro, uma incompatibilidade de formato, uma versão de cliente).
- Ação congelada em substantivo ("o processamento da sua requisição").
- 32 palavras, acima do limite de 25 para descrições.

Não marcado: "pode ter ocorrido" e "poderia ser causado por". Quem escreveu a mensagem é um sistema que não sabe o que deu errado. As duas ressalvas relatam essa incerteza com exatidão.

**Depois:**
> Sua requisição pode ter falhado. A causa pode ser um formato de dados diferente do formato que o servidor espera. Uma versão desatualizada do cliente pode causar essa diferença. Verifique a versão do cliente.

**Este exemplo é a razão de existir da regra da modalidade.** Uma reescrita tentadora troca a primeira frase por "Sua requisição falhou" e a terceira por "uma versão desatualizada do cliente **é a causa mais comum**". As duas trocas melhoram a leitura. As duas estão erradas. A primeira afirma uma falha de que o sistema só suspeita. A segunda inventa uma frequência que não aparece em lugar nenhum da entrada. Uma reescrita que fornece uma causa, uma frequência ou um mecanismo deixou de ser uma reescrita.

Em inglês, "may have failed" mantém uma forma composta que a regra dos tempos removeria. Em português, o conflito não aparece nesta frase: "pode ter falhado" usa o infinitivo composto depois do verbo modal, e a regra dos tempos visa outra forma ("tem falhado"). Nas duas línguas vale o mesmo princípio. **Quando a regra dos tempos e a regra da modalidade entram em conflito, a modalidade vence.** Tirar o auxiliar apagaria a incerteza junto com o tempo verbal.

### Exemplo C: instrução entre agentes

**Antes:**
> Uma vez que o job upstream tenha sido concluído e assumindo que nenhum erro tenha sido levantado, o agente downstream deverá proceder ao consumo do artefato de saída, sendo que vale ressaltar que artefatos parciais eventualmente são produzidos em condições de timeout.

**Violações marcadas:**
- Voz passiva e orações subordinadas empilhadas ("tenha sido concluído", "assumindo que...", "sendo que vale ressaltar que...").
- Decalques do inglês: "assumindo que" (assuming) e "eventualmente".
- Verbo-suporte ("proceder ao consumo") e expressão de preenchimento ("vale ressaltar que").
- Uma frase, três fatos separados (condição de término, próxima ação, aviso sobre um caso-limite).
- 42 palavras, acima do limite de 20 para instruções.

**Depois:**
> Espere o job upstream terminar sem erros. Depois, leia o artefato de saída. Atenção: um timeout pode produzir um artefato parcial. Verifique se o artefato está completo antes de usá-lo.

Decisões que vale a pena declarar em vez de esconder:
- "Deverá proceder ao consumo" virou o imperativo "leia". O STE permite essa troca em instruções, porque uma recomendação dirigida ao agente que executa a tarefa é uma ordem. Não faça a mesma troca em texto descritivo.
- "Uma vez que" tem duas leituras. Com o subjuntivo ("tenha sido concluído"), indica tempo ou condição. Com o indicativo, indica causa. A reescrita usa "Espere... terminar" e "Depois", que só têm a leitura de tempo.
- Aqui, "eventualmente" está certo em português ("às vezes"). Mas um leitor que pensa em inglês lê "eventually". A reescrita usa "pode", que tem uma leitura só.
- A última frase é **nova**. O original avisava sobre artefatos parciais, mas não dizia o que fazer. A verificação torna o aviso útil, mas é conteúdo acrescentado. Por isso, este exemplo declara a frase em vez de apresentá-la como reescrita. Se o silêncio da fonte era intencional, corte a frase.

### Exemplo D: prosa de README (modo Flexível)

**Antes:**
> Nossa camada de cache foi projetada para se encaixar perfeitamente na sua stack existente com o mínimo de atrito e sem vendor lock-in; ela alavanca a similaridade semântica para reduzir drasticamente os cache misses que tradicionalmente atormentam as cargas de trabalho de LLMs.

**Violações marcadas:**
- Adjetivos e afirmações de marketing sem medida ("perfeitamente", "com o mínimo de atrito", "drasticamente").
- Ponto e vírgula entre duas ideias separadas.
- Decalque e jargão ("alavanca", "vendor lock-in").
- Voz passiva ("foi projetada").
- 43 palavras, acima do limite de 25 para descrições.

**Depois:**
> Um cache comum compara as requisições pelo texto exato, então uma pequena mudança no texto causa um cache miss. Este cache compara o significado de um novo prompt com os prompts que ele já guarda. Ele funciona com a stack que você já usa e não prende você a um fornecedor.

O modo Flexível manteve o ritmo explicativo e não impôs um termo fixo por conceito. Ainda assim, ele cortou os adjetivos de marketing, o ponto e vírgula, o decalque e o excesso de palavras.

## Como ler estes exemplos

A Parte 1 mostra as regras do STE em que esta skill se baseia. A Parte 2 mostra as regras que o português acrescenta. A Parte 3 mostra a transferência para a saída de agentes. A mesma disciplina torna mais seguro de interpretar o texto entre máquinas e entre línguas, não só os manuais de aeronaves. Essa disciplina é: um significado por palavra, voz ativa, tempos simples, uma instrução por frase e condições explícitas em vez de orações subordinadas escondidas.
