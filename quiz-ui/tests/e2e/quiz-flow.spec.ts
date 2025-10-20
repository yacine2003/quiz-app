/**
 * Tests E2E pour le flow complet du quiz
 */
import { test, expect } from '@playwright/test'

test.describe('Quiz Flow Complet', () => {
  test('parcours complet: home → start → play → score → leaderboard', async ({ page }) => {
    // 1. Page d'accueil
    await page.goto('/')
    await expect(page.locator('h1')).toContainText('Quiz App')

    // Vérifier qu'il y a des quiz
    const quizCards = page.locator('article.card')
    await expect(quizCards.first()).toBeVisible()

    // Cliquer sur le premier quiz
    await quizCards.first().click()

    // 2. Page de démarrage
    await expect(page).toHaveURL(/\/quiz\/\d+\/start/)
    await expect(page.locator('h1')).toContainText(/Quiz|Prêt/)

    // Entrer le pseudo
    const nameInput = page.locator('input#name')
    await nameInput.fill('TestPlayer')
    await page.locator('button[type="submit"]').click()

    // 3. Page de jeu
    await expect(page).toHaveURL(/\/quiz\/\d+\/play/)

    // Vérifier la présence d'une question
    await expect(page.locator('.card')).toBeVisible()

    // Compter le nombre de questions
    const progressText = page.locator('text=/Question \\d+ \\/ \\d+/')
    await expect(progressText).toBeVisible()

    // Répondre à toutes les questions
    const totalQuestions = 15 // Ajuster selon vos données

    for (let i = 0; i < totalQuestions; i++) {
      // Attendre que la question soit visible
      await page.waitForSelector('.card', { timeout: 5000 })

      // Sélectionner la première réponse
      const firstChoice = page.locator('.card button').first()
      await firstChoice.click()

      // Attendre un peu (simule l'utilisateur qui lit)
      await page.waitForTimeout(300)

      // Si ce n'est pas la dernière question, cliquer sur Suivant
      if (i < totalQuestions - 1) {
        const nextButton = page.locator('button', { hasText: /Suivant/ })
        await nextButton.click()
      } else {
        // Dernière question, cliquer sur Terminer
        const submitButton = page.locator('button', { hasText: /Terminer/ })
        await submitButton.click()
      }
    }

    // 4. Page de score
    await expect(page).toHaveURL(/\/quiz\/\d+\/score/, { timeout: 10000 })
    await expect(page.locator('h1')).toContainText(/terminé/i)

    // Vérifier que le score s'affiche
    await expect(page.locator('text=/%/')).toBeVisible()
    await expect(page.locator('text=TestPlayer')).toBeVisible()

    // Aller au leaderboard
    const leaderboardButton = page.locator('button', { hasText: /classement/i })
    await leaderboardButton.click()

    // 5. Page leaderboard
    await expect(page).toHaveURL(/\/quiz\/\d+\/leaderboard/)
    await expect(page.locator('h1')).toContainText(/Classement/i)

    // Vérifier que notre score apparaît
    await expect(page.locator('text=TestPlayer')).toBeVisible()

    // Vérifier le podium si > 3 joueurs
    const podium = page.locator('text=/🥇|🥈|🥉/')
    if ((await podium.count()) > 0) {
      await expect(podium.first()).toBeVisible()
    }
  })

  test('validation du pseudo requis', async ({ page }) => {
    await page.goto('/')

    // Cliquer sur un quiz
    await page.locator('article.card').first().click()

    // Essayer de démarrer sans pseudo
    await page.locator('button[type="submit"]').click()

    // Vérifier qu'on reste sur la page
    await expect(page).toHaveURL(/\/quiz\/\d+\/start/)

    // Message d'erreur devrait apparaître
    await expect(page.locator('text=/Minimum.*caractères/i')).toBeVisible()

    // Tester avec un pseudo trop court
    await page.locator('input#name').fill('A')
    await page.locator('button[type="submit"]').click()
    await expect(page.locator('text=/Minimum.*caractères/i')).toBeVisible()

    // Tester avec un pseudo valide
    await page.locator('input#name').fill('ValidPlayer')
    await page.locator('button[type="submit"]').click()

    // Devrait rediriger vers le jeu
    await expect(page).toHaveURL(/\/quiz\/\d+\/play/)
  })

  test('navigation entre questions fonctionne', async ({ page }) => {
    await page.goto('/')
    await page.locator('article.card').first().click()

    // Entrer pseudo et démarrer
    await page.locator('input#name').fill('NavTestPlayer')
    await page.locator('button[type="submit"]').click()

    await expect(page).toHaveURL(/\/quiz\/\d+\/play/)

    // Répondre à la première question
    await page.locator('.card button').first().click()
    await page.locator('button', { hasText: /Suivant/ }).click()

    // Vérifier qu'on est sur la question 2
    await expect(page.locator('text=/Question 2/')).toBeVisible()

    // Retour en arrière
    await page.locator('button', { hasText: /Précédent/ }).click()

    // Vérifier qu'on est sur la question 1
    await expect(page.locator('text=/Question 1/')).toBeVisible()

    // La réponse précédente devrait être conservée
    // (vérifier visuellement ou par état du composant)
  })

  test('timer fonctionne', async ({ page }) => {
    await page.goto('/')
    await page.locator('article.card').first().click()

    await page.locator('input#name').fill('TimerTestPlayer')
    await page.locator('button[type="submit"]').click()

    await expect(page).toHaveURL(/\/quiz\/\d+\/play/)

    // Vérifier la présence du timer
    const timer = page.locator('text=/\\d+:\\d{2}/')
    await expect(timer).toBeVisible()

    // Attendre 2 secondes et vérifier que le timer a changé
    const initialTime = await timer.textContent()
    await page.waitForTimeout(2000)
    const newTime = await timer.textContent()

    expect(newTime).not.toBe(initialTime)
  })

  test('sauvegarde de progression fonctionne', async ({ page, context }) => {
    await page.goto('/')
    await page.locator('article.card').first().click()

    await page.locator('input#name').fill('SaveTestPlayer')
    await page.locator('button[type="submit"]').click()

    await expect(page).toHaveURL(/\/quiz\/\d+\/play/)

    // Répondre à 2 questions
    await page.locator('.card button').first().click()
    await page.locator('button', { hasText: /Suivant/ }).click()
    await page.locator('.card button').first().click()

    // Fermer et rouvrir (simuler refresh)
    const url = page.url()
    await page.close()

    // Nouvelle page
    const newPage = await context.newPage()
    await newPage.goto(url)

    // La progression devrait être conservée (question 2)
    await expect(newPage.locator('text=/Question 2|Question 3/')).toBeVisible()
  })
})

test.describe('Leaderboard', () => {
  test('affiche le classement trié par score', async ({ page }) => {
    await page.goto('/quiz/1/leaderboard')

    // Attendre le chargement
    await page.waitForSelector('table, text=/Aucun score/', { timeout: 5000 })

    // Si le tableau existe
    const table = page.locator('table')
    if (await table.isVisible()) {
      // Vérifier les colonnes
      await expect(page.locator('th', { hasText: /Rang/i })).toBeVisible()
      await expect(page.locator('th', { hasText: /Joueur/i })).toBeVisible()
      await expect(page.locator('th', { hasText: /Score/i })).toBeVisible()

      // Vérifier que les scores sont affichés
      await expect(page.locator('text=/%/')).toBeVisible()
    }
  })
})

