Feature: Login en OpenCart

  @Prueba2
  Scenario Outline: Login Exitoso
    Given Usuario ingresa nuevamente a la web de OpenCart "<url>"
    When Usuario da click en la opcion Login
    And Usuario ingesa su correo "<correo>"
    And Usuario ingresa su contraseña
    Then Se verifica el Login correcto

    Examples: 
      | url                            | nombre | apellido | correo               | telefono  |
      | https://opencart.abstracta.us/ | Juan   | Perez    | nuevo11@example.com  | 958025002 |
      | https://opencart.abstracta.us/ | Maria  | Lopez    | nuevo112@example.com | 999999999 |
