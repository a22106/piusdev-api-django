describe('QR Code Generator', () => {
  beforeEach(() => {
    cy.visit('http://localhost:5173')
    // Wait for the app to be fully loaded
    cy.contains('h1', 'QR Code Generator', { timeout: 10000 })
  })

  it('should load the application successfully', () => {
    cy.contains('h1', 'QR Code Generator')
    cy.get('input[type="radio"][value="url"]').should('be.visible')
  })

  it('should generate URL QR code', () => {
    cy.get('input[type="radio"][value="url"]').click()
    cy.get('input[name="url"]').type('https://example.com')
    cy.get('button[type="submit"]').click()
    
    // Wait for the API call and image to load
    cy.get('img[alt="Generated QR Code"]', { timeout: 10000 }).should('be.visible')
    cy.get('button').contains('Download PNG').should('be.enabled')
    cy.get('button').contains('Download SVG').should('be.enabled')
  })

  it('should generate Text QR code', () => {
    cy.get('input[type="radio"][value="text"]').click()
    cy.get('input[name="text"]').type('Hello World')
    cy.get('button[type="submit"]').click()
    
    // Wait for the API call and image to load
    cy.get('img[alt="Generated QR Code"]', { timeout: 10000 }).should('be.visible')
  })

  it('should generate Email QR code', () => {
    cy.get('input[type="radio"][value="email"]').click()
    cy.get('input[name="email"]').type('test@example.com')
    cy.get('input[name="subject"]').type('Test Subject')
    cy.get('textarea[name="body"]').type('Test Message')
    cy.get('button[type="submit"]').click()
    
    // Wait for the API call and image to load
    cy.get('img[alt="Generated QR Code"]', { timeout: 10000 }).should('be.visible')
  })

  it('should generate WiFi QR code', () => {
    cy.get('input[type="radio"][value="wifi"]').click()
    cy.get('input[name="ssid"]').type('MyWiFi')
    cy.get('input[name="password"]').type('password123')
    cy.get('select[name="encryption"]').select('WPA')
    cy.get('button[type="submit"]').click()
    
    // Wait for the API call and image to load
    cy.get('img[alt="Generated QR Code"]', { timeout: 10000 }).should('be.visible')
  })

  it('should handle form validation', () => {
    cy.get('input[type="radio"][value="url"]').click()
    cy.get('button[type="submit"]').click()
    // Check HTML5 validation
    cy.get('input[name="url"]').then($input => {
      expect(($input[0] as HTMLInputElement).validationMessage).to.not.be.empty
    })
  })

  it('should clear form when changing QR type', () => {
    cy.get('input[type="radio"][value="url"]').click()
    cy.get('input[name="url"]').type('https://example.com')
    cy.get('input[type="radio"][value="text"]').click()
    cy.get('input[name="text"]').should('be.empty')
  })

  it('should show error message on API failure', () => {
    cy.intercept('GET', 'http://localhost:8000/v1/qr/url/*', {
      statusCode: 500,
      body: 'Internal Server Error'
    }).as('generateQR')

    cy.get('input[type="radio"][value="url"]').click()
    cy.get('input[name="url"]').type('https://example.com')
    cy.get('button[type="submit"]').click()

    cy.wait('@generateQR')
    cy.contains('Failed to generate QR code', { timeout: 10000 }).should('be.visible')
  })
})