# 🔍 Analisador Léxico em Python

Este projeto implementa um **analisador léxico** (lexer) em Python para uma linguagem semelhante à **linguagem C**, responsável por ler o código-fonte e transformá-lo em uma sequência de **tokens**.

O lexer identifica números, identificadores, palavras reservadas, operadores, delimitadores, literais (`char`, `string`), diretivas de pré-processador e também detecta **erros léxicos**.

---

## 📌 Funcionalidades

- ✅ Identificação de **números inteiros e decimais**
- ✅ Suporte a **identificadores e palavras reservadas**
- ✅ Reconhecimento de **operadores** (1, 2 e até 3 caracteres)
- ✅ Delimitadores como `;`, `,`, `(`, `)`, `{`, `}`
- ✅ Literais de **caracteres** (`'a'`, `'\n'`, etc.)
- ✅ Literais de **strings** (`"Olá mundo"`)
- ✅ Diretivas de pré-processador (`#include`, `#define`, etc.)
- ✅ Suporte a **comentários** (`//` e `/* ... */`)
- 🚨 Detecção de **erros léxicos**:
  - Números malformados (ex: `123abc`)
  - Literais não terminados
  - Strings sem aspas finais
  - Char inválido (mais de 1 caractere)

