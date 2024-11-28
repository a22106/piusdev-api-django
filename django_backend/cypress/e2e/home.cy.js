describe('Home Page', () => {
  it('successfully loads', () => {
    cy.visit('/')
    cy.contains('QR Code Generator')
  })
})