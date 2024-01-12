Feature: Reachability of product catogries

  Scenario Outline: User navigates to different product categories
    Given I am a user of nbastore.eu
    When I visit nbastore.eu
    And I click on the <category> category
    Then I should be taken to the <category> category
    And the category should show at least 4 products
    When I click on the first product in the results
    Then I should be taken to the details page for that product
    Then I should close the browser

    Examples:
      | category |
      | Jerseys  |
      | Women    |
      | Footwear |
      | Men      |
      | Retro    | 