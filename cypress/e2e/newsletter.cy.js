describe('A formation leader...', () => {
    it('logs in', () => {
        cy.visit('/login/')
        cy.get('input[name="username"]').type('comms-cochair@example.com')
        cy.get('input[name="password"]').type('comms')
        cy.get('form').submit()
        // cy.visit('/formations/comms/').get('div.w-userbar-nav').should('exist')
    } )
} )
