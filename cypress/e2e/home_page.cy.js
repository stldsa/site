describe('The Home Page', () => {
    it('successfully loads', () => {
      cy.visit('/')
    })
  })


describe('The Admin Updates Page', () => {
  it('successfully loads', () => {
    cy.visit('/admin/updates')
  })
})