# AES-128
Replicação de uma criptografia do tipo Advanced Encryption Standard (AES) em Python.

## Informações gerais

 Esse projeto foi realizado como um trabalho semestral para a faculdade UNIP com o objetivo de entender o funcionamento da Advanced Encryption Standard (AES), 
uma das mais utilizadas e consolidadas na área da cibersegurança. Através do código desenvolvido por nós com base em documentos e fontes na internet, 
foi possível entender como a mensagem é alterada durante todo o processo, formando o texto cifrado. Foi escolhido a chave de 128 bits devido a sua 
praticidade, já que esse algoritmo não será implementado em nenhuma situação real.

 O programa possui uma interface gráfica onde é inserida uma chave de criptografia e a mensagem que será criptografada, exibindo o texto cifrado no canto inferior.
 
![interface de criptografia AES](https://github.com/dyaghas/aps-criptografia-aes/assets/56042071/3ac89bc9-5f2e-4404-9356-e04952bb2171)

## Como usar

O software possui um executável no diretório criptografia-aes/dist/main. Basta abrir esse arquivo

## Testes

 o Código implementa diversos tipos de testes para garantir o seu bom funcionamento. Por exemplo: teste unitário, de integração e de performance.


## Tecnologias

- Python
- Numpy
- Tkinter
- pytest

## Cenários de teste (em desenvolvimento)

https://docs.google.com/spreadsheets/d/1vvWNU1wLWs4oYRdJyBgaru2TH-YrHGpKjq81gGbbJIk/edit?usp=sharing

## 1 ADVANCED ENCRYPTION STANDARD (AES)

### 1.1 Fundamentos e conceitos
Por ser uma cifra de bloco simétrica, usa-se a mesma chave para encriptar e 
decriptar, sendo o comprimento da chave variável (128, 192, 256 bits) e o do bloco 
fixo em 128 bits. O design do AES é baseado em uma rede de substituição -
permutação - Substitution Permutation Network (SPN) - utilizando várias rodadas para 
criptografar os dados (10, 12 ou 14 rodadas, decidido a partir do comprimento da 
chave). Uma chave de 256 bits, considerado nível militar, é a mais forte e requer mais 
recursos para ser utilizada, consumindo mais bateria do dispositivo comparada à AES-128.

O processo da técnica AES se baseia em etapas e rodadas, a criptografia 
recebe o texto original e a chave, o texto original e chave são convertidos para 
hexadecimal e são transpostos em blocos de 16 bytes, 4 bytes de altura e 4 de largura. 
Cada caractere do texto original e da chave representa um byte na grade 4x4, e caso 
o texto original exceda um bloco, outros serão criados.

Após isso se inicia a etapa Sub-Byte, onde o algoritmo substitui cada byte por 
um código, de acordo com uma tabela pré-estabelecida chamada Rijndael S-box.
Na etapa Shift Rows, ocorre a transposição em que as três últimas linhas do 
estado são deslocadas ciclicamente em um certo número de etapas. A primeira linha 
permanece no lugar, no entanto, a segunda linha é deslocada para a esquerda em um 
byte, a terceira linha se move para a esquerda em dois bytes, enquanto a última é 
deslocada em três bytes ou simplesmente um byte para a direita, tendo o mesmo 
efeito.

Na etapa Mix columns, multiplica-se uma matriz constante com cada coluna no 
bloco para obter uma nova coluna para o bloco subsequente. Uma vez que todas as 
colunas são multiplicadas com a mesma matriz constante, você obtém seu bloco para 
a próxima etapa.

Na etapa Add Round Key, a subchave é combinada com o bloco, para cada 
rodada, uma subchave é derivada da chave principal usando o Rijndael's key 
schedule, cada subchave é do mesmo tamanho que o bloco. A subchave é adicionada 
combinando cada byte do estado com o byte correspondente da subchave usando 
XOR bit a bit.

### 1.2 Benefícios
As rodadas de criptografia são a razão por trás da impenetrabilidade do AES, 
pois há muitas rodadas para quebrar. Sendo assim o processo de criptografia do AES 
é relativamente fácil de entender. Isso permite uma implementação fácil, bem como 
tempos de criptografia e descriptografia realmente rápidos.
Além disso, o AES requer menos memória do que muitos outros tipos de 
criptografia (como DES), o que o torna um verdadeiro vencedor quando se trata de 
escolher seu método de criptografia preferido. Além de tudo, quando uma ação requer 
uma camada extra de segurança, você pode combinar o AES com vários protocolos 
de segurança como WPA2 ou até mesmo outros tipos de criptografia como SSL.

### 1.3 Aplicações
Alguns VPNs que usam AES com chaves de 256 bits incluem NordVPN, 
Surfshark e Express VPN. Redes sem fio também utilizam criptografia AES 
(geralmente, junto com o protocolo WPA2). Muitos aplicativos de celular populares,
(como por exemplo, Snapchat e Facebook Messenger) fazem uso da criptografia AES 
para o envio de informações com segurança, como fotos e mensagens. Além disso, 
alguns componentes do sistema operacional, (como sistemas de arquivos) também 
usufruem do padrão de criptografia avançado para uma camada extra de segurança.
Enfim, as bibliotecas de linguagens de codificação como Java, Python e C++ 
implementam a criptografia AES. Também é possível encontrar a técnica criptográfica 
AES em diversos navegadores da web.

### 1.4 Comparação entre AES e outras técnicas
O AES (Advanced Encryption Standard), assim como o DES (Data Encryption 
Standard) e 3DES (Triple Data Encryption Standard), trabalha com blocos de 
informação e chave simétricos. O AES possui uma única chave que é utilizada tanto 
no momento de criptografia, quanto no momento de descriptografia da mensagem e, 
assim como os antigos DES e 3DES, o processo de “embaralhamento” de 
informações” passa por rounds (rodadas) que realizam o procedimento mais de uma 
vez. 

Entretanto, diferentemente do DES e 3DES, por exemplo, o método AES separa 
a mensagem em blocos simétricos de 128-bit em vez de 64-bit, e sua chave pode ser 
de 128, 192 ou 256-bit, e não de 56-bit como no DES. Por conta de sua maior chave 
e método de substituição e permutação de informações, o padrão AES tornou-se 
muito mais seguro e rápido quando comparado à estas criptografias.
Comparando o AES, que utiliza chave única, com o sistema RSA (Rivest–
Shamir–Adleman), que utiliza uma chave pública para criptografia e uma chave 
privada para descriptografia, o AES se mostrou mais efetivo em testes de segurança, 
mesmo o RSA utilizando chaves de 2048 e 4096-bit. Assim, fazendo com que o padrão 
AES fosse utilizado até mesmo em grandes estatais pelo mundo.

### 1.5 Vulnerabilidades e falhas
Há uma classe de vulnerabilidades conhecidas no mundo da criptografia como 
“padding oracle attacks”, é o método mais otimista para tentar realizar a quebra da 
criptografia AES. Estes ataques consistem em descobrir um padrão nas mensagens 
criptografadas a partir de textos comuns que podem estar presentes na comunicação,
o hacker intercepta a mensagem e testa cada bloco de informação, alterando valores
e verificando se houve erro no novo resultado (prática man-in-the-middle), assim 
quebrando a segurança existente.

### 1.6 Melhorias propostas ou implementadas
O método de criptografia utilizado neste trabalho (AES-128) possui 2128
possibilidades de chave, o que é mais do que suficiente para nenhum computador 
moderno consiga quebrar a segurança. Porém, com o desenvolvimento de 
computadores quânticos, o poder de processamento de dados ficará milhões de vezes 
mais rápido, ameaçando a integridade das criptografias atuais, e até mesmo 
criptografias que utilizam bloco simétrico, como a AES, poderiam ser quebradas após 
algum tempo. Falhas humanas como: utilizar uma mesma chave para uma larga linha 

de produtos, também são preocupantes para quem preza e trabalha com segurança 
da informação. Pensando nisso, o método mais eficiente a curto prazo é dobrar o 
tamanho das chaves em criptografia de bloco simétrico, utilizando algo como “AES512”, dificultando até mesmo para um computador quântico processar todas as 
possibilidades de chave. 

Implementar o procedimento de Encrypt-then-MAC (EtM) melhoraria muito a 
segurança, impossibilitando até mesmo que estratégias como o man-in-the-middle 
fossem efetivas. O EtM consiste em gerar uma mensagem de autenticação (Message 
authentication code - MAC), baseada na informação criptografada, utilizando uma 
segunda chave junto a uma função Hash para gerar a MAC. Assim a autenticidade da 
informação inicial seria verificada e seria garantido que não houve alteração, além de 
que só quem possui a chave MAC consiga ler as informações.

## 2 ESTRUTURA DO PROGRAMA

### 2.1 Funcionamento
Antes de iniciar o processo de criptografia, é necessário preparar o texto 
simples e a chave de criptografia que será utilizada. Ambos são armazenados em 
blocos de 16 bytes, cada célula armazenando um caractere. Como os dois 
possivelmente terão mais de 16 caracteres, são armazenados fragmentos em 
diversos blocos. Para a chave há um processo extra chamado expansão de chave, 
que ocorre uma vez para cada rodada da criptografia. (SIMPLILEARN, 2022; 
CYBERNEWS, 2022, tradução nossa).

Imagem 1 - Texto em bloco

![image](https://github.com/dyaghas/aps-criptografia-aes/assets/56042071/fbed93b2-3fbe-4940-a404-f0b7e9a2d018)

(Fonte: autoria própria)

Como pode ser visto na imagem acima, a mensagem “Two One Nine Two” é 
armazenada em um bloco, incluindo os espaços.

### 2.2 Add Round Key
A primeira etapa desse padrão de criptografia é chamada “add round key”, 
consistindo em um XOR entre o bloco da chave secreta e da mensagem que será 
criptografada. Ao realizar esse processo com a chave “Thats my kung fu” e a 
mensagem “Two One Nine Two” o resultado será “00 3c 6e 47 3c 4e 22 74 6e 22 1b 
31 47 74 31 1a”. Para que esse processo seja possível, é preciso primeiro que todos 
os caracteres sejam convertidos para valores numéricos conforme a tabela ASCII 
(American Standard Code for Information Interchange). Após os valores serem 
convertidos para hexadecimal, as matrizes foram transpostas para facilitar a 
manipulação dos dados em etapas futuras.

Imagem 2 – Add round key

![image](https://github.com/dyaghas/aps-criptografia-aes/assets/56042071/dffd0a2a-2175-4331-9d12-3ddf21cf7108)

(Fonte: autoria própria)

Tabela 1 – Tabela ASCII

![image](https://github.com/dyaghas/aps-criptografia-aes/assets/56042071/bc194aca-b664-4c8b-915f-b25eabeae80f)

(Fonte: Alpharithms, 2022.)

### 2.3 Byte Sub
A substituição dos bytes é realizada através de uma comparação entre a saída 
do passo anterior e uma tabela chamada S-box. Para manter a simplicidade e evitar 
possíveis problemas na implementação e segurança da criptografia, foi utilizado a 
23
S-box de Rijndael. Os valores em hexadecimal são comparados aos índices da S-box 
e trocado pelo valor presente no índice encontrado.

Tabela 2 – Rijndael S-box

![image](https://github.com/dyaghas/aps-criptografia-aes/assets/56042071/ca2cc623-bd01-44dc-a392-1e106ca87a53)

 
(Fonte: Wikipedia)
 
Seguindo a tabela, o valor de entrada b4 retornaria 8d, que é o valor presente 
na linha b e coluna 4. Assim sendo, o resultado dessa operação no bloco 00 3c 6e 47 
3c 4e 22 74 6e 22 1b 31 47 74 31 1a será 63 eb 9f a0 eb 2f 93 92 9f 93 af c7 a0 92 c7 
a2.

Imagem 3 – Byte sub

![image](https://github.com/dyaghas/aps-criptografia-aes/assets/56042071/1b4659e4-bb01-4cb8-aaa8-0cf3be51b82d)

 
(Fonte: autoria própria)
 
### 2.4 Shift Row
Realiza um deslocamento em cada linha da matriz, mantendo a primeira linha 
e jogando os elementos das linhas seguintes para a esquerda (CYBERNEWS, 2022, 
tradução nossa).
Linha 0: n = n – 0
Linha 1: n = n – 1
Linha 2: n = n – 2
Linha 3: n = n – 3

Imagem 4 – Shift Row

![image](https://github.com/dyaghas/aps-criptografia-aes/assets/56042071/912fa798-8d06-43a7-a5ff-58930e2cc70d)
 
(Fonte: autoria própria)

### 5.5 Mix Columns
A última etapa da criptografia realiza multiplicações entre a saída do passo 
anterior e uma matriz de multiplicação predefinida. Os valores obtidos são colocados 
em um Campo de Galois, que nesse caso é representado por duas tabelas: Tabela L 
e Tabela E.

Imagem 7 – Mix Columns

![image](https://github.com/dyaghas/aps-criptografia-aes/assets/56042071/438d83fa-4bc5-4665-a6a9-62bb5d9031ac)

(Fonte: autoria própria)

Tabela 3 – Tabela E

![image](https://github.com/dyaghas/aps-criptografia-aes/assets/56042071/4be27ccd-e47d-4df2-a3ef-40d160640a85)


(Fonte: AES (Advanced Encryption Standard) Simplified)
 
Tabela 4 – Tabela L

![image](https://github.com/dyaghas/aps-criptografia-aes/assets/56042071/8f5cafe4-b34d-4b35-9af1-e03e98279e2a)


(Fonte: AES (Advanced Encryption Standard) Simplified)
 
Para obter a primeira linha da matriz resultante, é feito os seguintes cálculos:

Figura 1 - Multiplicação entre state_array e matriz de multiplicação

![image](https://github.com/dyaghas/aps-criptografia-aes/assets/56042071/51e39693-1bdd-4f03-af8c-48a7bd68c392)

(Fonte: autoria própria)


Saída(00) = E(L(63) + L(02)) ⊕ E(L(2f) + L(03)) ⊕ E(L(af) + L(01)) ⊕ E(L(a2) + L(01)) =

E(c3 + 19) ⊕ E(78 + 01) ⊕ E(b7 + 00) ⊕ E(f6 + 00) =

E(dc) ⊕ E(79) ⊕ E(b7) ⊕ E(f6) =

c6 ⊕ 71 ⊕ af ⊕ a2 = ba

Saída(01) = E(L(63) + L(01)) ⊕ E(L(2f) + L(02)) ⊕ E(L(af) + L(03)) ⊕ E(L(a2) + L(01)) = 

E(c3 + 00) ⊕ E(78 + 19) ⊕ E(b7 + 01) ⊕ E(f6 + 00) =

E(c3) ⊕ E(91) ⊕ E(b8) ⊕ E(f6) =

63 ⊕ 5e ⊕ ea ⊕ a2 = 75

Saída(02) = E(L(63) + L(01)) ⊕ E(L(2f) + L(01)) ⊕ E(L(af) + L(02)) ⊕ E(L(a2) + L(03)) = 

E(c3 + 00) ⊕ E(78 + 00) ⊕ E(b7 + 19) ⊕ E(f6 + 01) =

E(c3) ⊕ E(78) ⊕ E(d0) ⊕ E(f7) =

63 ⊕ 2f ⊕ 45 ⊕ fd = f4

Saída(03) = E(L(63) + L(03)) ⊕ E(L(2f) + L(01)) ⊕ E(L(af) + L(01)) ⊕ E(L(a2) + L(02)) = 

E(c3 + 01) ⊕ E(78 + 00) ⊕ E(b7 + 00) ⊕ E(f6 + 19) =

E(c4) ⊕ E(78) ⊕ E(b7) ⊕ E(10f) =

Subtrai FF de 10F (10F é maior do que FF)

E(c4) ⊕ E(78) ⊕ E(b7) ⊕ E(10f - ff) =

E(c4) ⊕ E(78) ⊕ E(b7) ⊕ E(10) =

a5 ⊕ 2f ⊕ af ⊕ 5f = 7a

Resultado:

Coluna 1 = [ba, 75, f4, 7a]

Esse mesmo processo é repetido para as outras três colunas.
