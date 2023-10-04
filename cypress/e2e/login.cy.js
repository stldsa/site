describe('Logging In', function () {

    it('on login page', () => {
        cy.visit('/login/')
        cy.get('#id_username').type('admin@example.com')
        cy.get('#id_password').type(`password{enter}`)        
    })
})
