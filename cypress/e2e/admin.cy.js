describe('The superadmin account...', () => {
    it ('logs in', () => {
        cy.visit('/login/')
        cy.get('input[name="username"]').type('admin@example.com')
        cy.get('input[name="password"]').type('stldsa')
        cy.get('form').submit()
        cy.url().should('include', '/myDSA/')
        cy.visit('/admin/formations/add')
    })
})