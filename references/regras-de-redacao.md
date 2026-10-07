# Regras de redação: resumo, adaptação ao português e fontes

Este arquivo resume a descrição pública e oficial do ASD-STE100 (Simplified Technical English). Ele parafraseia as *categorias* de regras. Ele não reproduz o texto da norma nem o dicionário de cerca de 900 palavras. Para o documento oficial, peça o download gratuito no site oficial. O arquivo descreve também como esta skill adapta cada regra ao português do Brasil e quais referências brasileiras ela usa.

## O que é o ASD-STE100

O ASD-STE100 é uma linguagem natural controlada. A primeira versão saiu em 1986, como o documento AECMA PSC-85-16598. A organização que publicou a norma hoje se chama ASD (AeroSpace and Defence Industries Association of Europe). As companhias aéreas europeias pediram a norma. Muitas das equipes delas não falavam inglês como língua materna e precisavam de uma documentação de manutenção que ninguém pudesse ler errado. Numa aeronave, uma instrução mal lida pode matar.

O Simplified Technical English Maintenance Group (STEMG) mantém a norma. O download é gratuito desde o Issue 6 (2013). A edição atual é o Issue 9 (janeiro de 2025).

## Estrutura

- **53 regras de redação em 9 seções**: escolha de palavras, gramática, estrutura da frase e estilo.
- **Um dicionário** de cerca de 900 palavras aprovadas, cada uma restrita a um significado e a uma classe gramatical. O dicionário lista também cerca de 1.200 palavras a evitar, com substitutas sugeridas.
- **Uma permissão de terminologia**: uma organização pode definir um dicionário próprio de substantivos e verbos técnicos aprovados, além das 900 palavras de base. Esse dicionário próprio cobre o vocabulário de domínio que o dicionário-base não tem.

## Categorias de regras (paráfrase)

**Escolha de palavras**
- Use as palavras aprovadas só no significado e na classe gramatical aprovados.
- Cada palavra corresponde a um só significado. Não dependa do contexto para resolver uma palavra que tem vários sentidos no dicionário.
- Prefira a palavra mais simples, curta e comum a um sinônimo formal ou raro.
- Use um verbo aprovado para uma ação, não um substantivo derivado desse verbo (Regra 3.7).
- Não forme phrasal verbs, isto é, um verbo junto de uma preposição (Regra 9.3). As partes não permitem prever o sentido deles, e tanto leitores não nativos quanto sistemas de tradução erram com eles.

**Formas verbais**
- Formas permitidas: infinitivo, imperativo, presente simples, passado simples, futuro simples e particípio passado usado só como adjetivo.
- Sem present perfect, past perfect nem outras construções compostas ou com auxiliar. "We have received" não é permitido. "We received" é permitido.
- As formas em "-ing" são permitidas só como substantivo técnico ou como parte de um, não como forma verbal.

**Voz**
- A voz ativa é obrigatória em procedimentos e instruções.
- A voz passiva só é permitida em texto descritivo, e só quando quem age é de fato desconhecido ou irrelevante para o leitor.

**Estrutura da frase**
- Uma instrução por frase.
- No máximo cerca de 20 palavras por frase em procedimentos e instruções. No máximo cerca de 25 em texto descritivo.
- Não omita partes da frase (verbo, sujeito, artigo) só para encurtá-la. A norma avisa que essa omissão cria ambiguidade em vez de clareza.
- Grupos nominais (substantivos empilhados como modificadores) têm no máximo 3 palavras.
- O ponto e vírgula não é permitido (Regra 8.1): "You can use all standard English punctuation marks but not the semicolon (;)." Isto é, todos os sinais de pontuação padrão do inglês são permitidos, menos o ponto e vírgula. Escreva frases separadas. Todos os outros sinais continuam permitidos, inclusive o travessão.

**Estrutura do parágrafo e do documento**
- Um tópico por parágrafo.
- No máximo cerca de 6 frases por parágrafo.
- Use listas verticais (numeradas ou com marcadores) para sequências, condições ou enumerações complexas. Não esconda essas sequências na prosa.

**Instruções de segurança**
- Uma instrução crítica para a segurança começa com um comando ou uma condição clara. Ela não fica escondida no meio da frase.

## Adaptação ao português

O STE foi escrito para o inglês. Algumas regras passam direto para o português, outras mudam de forma. O português tem também fontes de ambiguidade que o inglês não tem. A tabela mostra como esta skill trata cada caso.

| Regra do STE | No português | Por quê |
|---|---|---|
| Uma palavra, um significado | Igual. Sem dicionário aprovado, vale só a consistência dentro do documento. | Não existe dicionário controlado para o português. |
| Verbo, não substantivo (3.7) | Igual, com foco no verbo-suporte: "realizar a análise", "efetuar o pagamento", "proceder à remoção", "fazer uso de". | O verbo-suporte é a forma mais comum de nominalização no português técnico e administrativo. |
| Sem phrasal verbs (9.3) | Não se aplica. No lugar dela: sem locuções prolixas ("a fim de", "tendo em vista que", "no que diz respeito a", "sendo que", "encontra-se"). | O português não tem phrasal verbs. A locução prolixa é o vício mais próximo: várias palavras no lugar de uma. |
| Tempos simples | O pretérito perfeito simples cobre o present perfect. "Tem" + particípio indica repetição, não ação concluída. O subjuntivo é obrigatório em condições. Sem gerundismo. | O pretérito perfeito composto do português tem outro sentido. Traduzir o present perfect por ele muda a afirmação. |
| Formas em "-ing" | Gerúndio só para ações simultâneas. Sem gerúndio depois de vírgula para ações em sequência ou para consequências. | A oração reduzida de gerúndio não diz a relação entre as duas ações. |
| Voz ativa | Igual. A regra inclui a passiva sintética ("Exclui-se o arquivo", "Recomenda-se"). | A partícula "se" também esconde quem age. |
| Grupos nominais de até 3 palavras | No máximo três "de" seguidos. | O português não empilha substantivos. O equivalente é a cadeia de "de". |
| Sem omissões | Igual. O sujeito fica explícito sempre que muda. | O português permite sujeito oculto. Quando o sujeito muda, o leitor não sabe quem age. |
| Sem ponto e vírgula (8.1) | Igual, inclusive nos itens de lista no estilo jurídico. | A regra não depende do idioma. |
| Tamanho da frase | Igual: 20 e 25 palavras. | O português costuma usar algumas palavras a mais que o inglês para a mesma ideia (artigos, preposições). A skill mantém os limites do STE. A opção `--max-palavras` ajusta o linter quando um projeto decide outro limite. |
| Sem equivalente no STE | "Dever" ambíguo: ordem ou estimativa. | "O job deve terminar em 5 minutos" tem duas leituras. A regra da modalidade proíbe escolher uma delas em silêncio. |
| Sem equivalente no STE | "Seu" ou "sua" com dois donos possíveis, e "o mesmo" no lugar de pronome. | "Seu" pode se referir a você ou a qualquer terceira pessoa da frase. |
| Sem equivalente no STE | Tratamento uniforme: "você" e imperativo ("Remova"), sem mistura com "tu" ("Remove") nem com o infinitivo ("Remover"). | "Remove o arquivo" pode ser uma ordem (tu) ou uma descrição ("ele remove o arquivo"). O leitor não sabe qual das duas. |
| Sem equivalente no STE | Decalques do inglês e falsos cognatos: "eventualmente", "assumir que", "endereçar", "suportar", "uma vez que". | Um leitor que pensa em inglês entende um sentido, e um leitor que pensa em português entende outro. |
| Sem equivalente no STE | Siglas por extenso na primeira ocorrência. | A Lei 15.263 pede o nome completo antes das siglas (Art. 5º, VIII). |

## Referências brasileiras

Não existe uma linguagem controlada oficial para o português. Além do STE, esta skill usa as referências brasileiras abaixo.

**Lei nº 15.263, de 14 de novembro de 2025.** A lei institui a Política Nacional de Linguagem Simples nos órgãos e entidades da administração pública. O Art. 4º define linguagem simples como "o conjunto de técnicas destinadas à transmissão clara e objetiva de informações, de modo que as palavras, a estrutura e o leiaute da mensagem permitam ao cidadão facilmente encontrar a informação, compreendê-la e usá-la". O Art. 5º lista as técnicas. Vários incisos coincidem com regras desta skill:

| Inciso do Art. 5º (texto da lei) | Regra desta skill |
|---|---|
| I: "redigir frases em ordem direta" | Ordem direta, sem intercaladas |
| II: "redigir frases curtas" | Tamanho da frase |
| III: "desenvolver uma ideia por parágrafo" | Limites de parágrafo |
| IV: "usar palavras comuns, de fácil compreensão" | Uma palavra, um significado (direção) |
| V: "usar sinônimos de termos técnicos e de jargões ou explicá-los no próprio texto" | Termos de domínio |
| VI: "evitar palavras estrangeiras que não sejam de uso corrente" | Estrangeirismos e falsos cognatos |
| VIII: "redigir o nome completo antes das siglas" | Siglas |
| IX: "organizar o texto de forma esquemática, quando couber, com o uso de listas, tabelas e recursos gráficos" | Listas para sequências |
| XII: "redigir frases preferencialmente na voz ativa" | Voz ativa |
| XIII: "evitar frases intercaladas" | Ordem direta, sem intercaladas |
| XIV: "evitar o uso de substantivos no lugar de verbos" | Verbo pleno, sem verbo-suporte |
| XV: "evitar redundâncias e palavras desnecessárias" | Sem locuções prolixas |
| XVI: "evitar palavras imprecisas" | Uma palavra, um significado |

A lei vale para os textos da administração pública dirigidos ao cidadão. Esta skill não é um instrumento de conformidade com a lei. Ela usa os incisos como evidência de que as regras do STE fazem sentido em português.

**ABNT NBR ISO 24495-1:2024.** A versão brasileira da ISO 24495-1:2023 (linguagem simples, parte 1: princípios e diretrizes norteadores) saiu em julho de 2024. A norma tem quatro princípios. O leitor recebe o que precisa (relevante), encontra o que precisa (localizável), entende o que encontra (compreensível) e consegue usar a informação (utilizável). A norma ISO diz que vale também para a redação técnica e para o uso de linguagens controladas. Ela se aplica à maioria das línguas escritas, mas dá exemplos só em inglês.

**Manual de Comunicação da Secom do Senado Federal.** O verbete "mesmo" orienta: "Não use *o mesmo*, *a mesma* para substituir nomes e pronomes." A regra de referência sem ambiguidade desta skill segue essa orientação.

**Acordo Ortográfico e VOLP.** A ortografia segue o Acordo Ortográfico da Língua Portuguesa de 1990, que o Decreto nº 6.583/2008 promulgou no Brasil. Ela segue também o Vocabulário Ortográfico da Língua Portuguesa (VOLP), da Academia Brasileira de Letras. A própria Lei 15.263 cita os dois (Art. 5º, XI).

## Por que esta skill usa o STE para a saída de agentes

O STE evita a ambiguidade para um leitor que não pode fazer uma pergunta de volta. Esse leitor é um técnico na pista, com um manual na mão e sem um autor para consultar. Um agente de IA que lê a saída de outro agente, a descrição de uma ferramenta ou uma mensagem de sistema está na mesma posição. Ele não tem um canal de volta para resolver uma dúvida. Por exemplo: esta frase na voz passiva quer dizer que quem chama faz X, ou que quem é chamado faz X? As regras que impedem um mecânico de ler errado uma especificação de torque impedem também um agente de ler errado uma instrução.

Em português há um motivo a mais. Os modelos de linguagem aprendem sobretudo com texto em inglês, e o português que eles escrevem traz decalques do inglês. Um decalque pode ter um sentido para quem lê pelo inglês e outro para quem lê pelo português. "Eventualmente" é o caso típico: em português, a palavra quer dizer "às vezes", e quem pensa em "eventually" lê "mais cedo ou mais tarde". As regras próprias do português nesta skill removem essa leitura dupla.

## Fontes

**STE**
- [Site oficial do ASD-STE100](https://www.asd-ste100.org/)
- [ASD-STE100: About STE](https://www.asd-ste100.org/about_STE.html)
- [ASD Europe: Simplified Technical English](https://www.asd-europe.org/standards-specifications/simplified-technical-english/)
- [Simplified Technical English na Wikipedia](https://en.wikipedia.org/wiki/Simplified_Technical_English)
- [TechScribe: ASD-STE100 Simplified Technical English](https://www.techscribe.co.uk/techw/asd-simplified-technical-english.htm)
- [SKYbrary: Simplified Technical English (STE)](https://skybrary.aero/articles/simplified-technical-english-ste)

**Brasil e linguagem simples**
- [Lei nº 15.263, de 14 de novembro de 2025 (Câmara dos Deputados, publicação original)](https://www2.camara.leg.br/legin/fed/lei/2025/lei-15263-14-novembro-2025-798293-publicacaooriginal-177011-pl.html)
- [ISO 24495-1:2023, Plain language, Part 1: Governing principles and guidelines](https://www.iso.org/standard/78907.html)
- [Manual de Comunicação da Secom do Senado Federal: verbete "mesmo"](https://www12.senado.leg.br/manualdecomunicacao/estilos/mesmo)
- [Academia Brasileira de Letras (VOLP)](https://www.academia.org.br/)
