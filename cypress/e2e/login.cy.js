describe('/login', () => {

    beforeEach(() => {
        cy.visit('/login/')
    })

    it('greets with Sign In', () => {
        cy.contains('h1', 'Log In')
    })

    it ('links to /signup', () => {
        cy.contains('Sign up here').should('have.attr', 'href', '/signup/')
    })

    // it('requires email', () => {
    //     cy.get('form').contains('Log In').click()
    //     cy.get('.error-messages').should('contain', 'email con\'t be blank')
    // })
    //     cy.get('#id_username').type('admin@example')
    //     cy.get('.errorlist').should('have.length', 1)
    // })
    // it('requires password', () => {
    //     cy.get('#id_username').type('admin@example')
    //     cy.get('.errorlist').should('have.length', 1)
    // })
    it ('logs in', () => {
        cy.get('input[name="username"]').type('admin@example.com')
        cy.get('input[name="password"]').type('stldsa')
        cy.get('form').submit()
        cy.location('href').should('eq', 'http://localhost:8000/myDSA/')
    })
})

describe('Member Login', () => {
    
    it ('logs in', () => {
        cy.visit('/login/')
        cy.get('input[name="username"]').type('member@example.com')
        cy.get('input[name="password"]').type('PRZ9L!vEJXeid-4')
        cy.get('form').submit()
        cy.location('href').should('eq', 'http://localhost:8000/myDSA/')
    })

})