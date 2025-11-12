# Padronizações

## Funções
1. Colocar nome das funções em snake_case
    ```python
    def exemplo_snake()
    ```
2. Tipar variáveis e retorno esperado
    ```python
    def soma_valores(v: int, v2:int) -> int:
    ```
3. Criar métodos que executam apenas 1 funcionalidade
    ```python
    def soma_e_subtrai() #ta errado paizao
    ```

## Classes
1. Colocar nomes em camelCase
    ```python
    class testeClasse
    ```

## Interface visual (pygame)
- Componentes Pygame ficam em `modules/ui`
- O módulo expõe classes reutilizáveis: `PropertyCard`, `EventCard`, `HouseToken` e `GameBoard`
- Execute `python -m modules.ui.demo` para visualizar um exemplo rápido
- Inicialize o pygame antes de usar (`pygame.init()`), depois crie e desenhe os componentes na sua janela
