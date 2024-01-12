Feature: Search functionality

    Scenario: Search for Michael Jordan
        Given I am a user of the nbastore.eu
        When I visit the nbastore.eu
        And I search for a product using the term Michael Jordan
        Then I should see the search results
        And there should be at least 5 products in the search results
        When I click on the first product in the results
        Then I should be taken to the details page for that product
        Then close the browser