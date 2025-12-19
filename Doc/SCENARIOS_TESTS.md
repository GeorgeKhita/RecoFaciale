# 🧪 SCÉNARIOS DE TESTS - Système de Cantine RecoFacial

## Vue d'ensemble

Ce document décrit les scénarios de tests essentiels pour valider le bon fonctionnement du système.

---

## 1. Test d'ajout d'un nouvel étudiant

**Étapes :**
1. Cliquer sur "➕ Nouvel Utilisateur"
2. Saisir le nom : "Pierre Dupont"
3. Saisir le solde initial : 50.00€
4. Se placer face à la caméra et bouger légèrement
5. Attendre la capture de 30 photos

**Résultats attendus :**
- ✅ Message de succès : "✅ Pierre Dupont ajouté avec succès!"
- ✅ "Pierre Dupont" apparaît dans la liste des comptes avec solde 50.00€
- ✅ Dossier `face_samples/Pierre Dupont/` créé avec 30 photos

---

## 2. Test de reconnaissance faciale

**Préconditions :**
- Étudiant "Pierre Dupont" enregistré

**Étapes :**
1. Se placer face à la caméra (en tant que Pierre Dupont)
2. Attendre la détection du visage

**Résultats attendus :**
- ✅ Rectangle vert autour du visage
- ✅ Nom "Pierre Dupont" affiché
- ✅ Message : "✅ Pierre Dupont reconnu" ou "✅ Pierre Dupont débité!"

---

## 3. Test de reconnaissance d'une personne inconnue

**Étapes :**
1. Se placer face à la caméra (personne non enregistrée)

**Résultats attendus :**
- ✅ Rectangle rouge autour du visage
- ✅ Texte "Inconnu" affiché
- ✅ Message : "❌ Personne non reconnue"

---

## 4. Test de débit automatique

**Préconditions :**
- Mode AUTO activé
- Étudiant "Pierre Dupont" avec solde 50.00€
- `last_debit_date` != aujourd'hui

**Étapes :**
1. Se placer face à la caméra (en tant que Pierre Dupont)
2. Attendre la reconnaissance

**Résultats attendus :**
- ✅ Message : "✅ Pierre Dupont débité!\n-3.50€\nNouveau solde: 46.50€"
- ✅ Solde mis à jour dans la liste des comptes

**Vérifications :**
- [ ] Dans `accounts.json` : solde = 46.5
- [ ] Transaction ajoutée dans l'historique

---

## 5. Test de débit déjà effectué aujourd'hui

**Préconditions :**
- Mode AUTO activé
- Étudiant "Pierre Dupont" déjà débité aujourd'hui

**Étapes :**
1. Se placer face à la caméra (en tant que Pierre Dupont)

**Résultats attendus :**
- ✅ Rectangle orange avec "Pierre Dupont - DÉJÀ DÉBITÉ"
- ✅ Message : "⏳ Pierre Dupont a déjà été débité aujourd'hui"
- ✅ Solde inchangé

---

## 6. Test de débit manuel

**Préconditions :**
- Mode MANUEL activé
- Étudiant "Pierre Dupont" reconnu

**Étapes :**
1. Se placer face à la caméra
2. Attendre la reconnaissance
3. Cliquer sur "💳 DÉBITER MAINTENANT"

**Résultats attendus :**
- ✅ Message de succès : "✅ 3.50€ débités de Pierre Dupont"
- ✅ Solde mis à jour

---

## 7. Test d'ajout de crédit

**Préconditions :**
- Étudiant "Pierre Dupont" avec solde 20.00€

**Étapes :**
1. Cliquer sur "💰 Ajouter Crédit"
2. Sélectionner "Pierre Dupont"
3. Saisir le montant : 25.00€
4. Cliquer sur "Ajouter"

**Résultats attendus :**
- ✅ Message : "✅ 25.00€ ajoutés à Pierre Dupont"
- ✅ Solde mis à jour : 45.00€

---

## 8. Test de consultation des comptes

**Préconditions :**
- Au moins 2 étudiants enregistrés

**Étapes :**
1. Cliquer sur "📊 Voir Comptes"

**Résultats attendus :**
- ✅ Fenêtre s'ouvre avec la liste de tous les comptes
- ✅ Format : "Nom" | "Solde"
- ✅ Soldes corrects

---

## 9. Test de suppression d'un utilisateur

**Préconditions :**
- Étudiant "Pierre Dupont" enregistré

**Étapes :**
1. Cliquer sur "🗑️ Supprimer un utilisateur"
2. Saisir : "Pierre Dupont"
3. Confirmer la suppression

**Résultats attendus :**
- ✅ Message : "Pierre Dupont a été supprimé avec succès."
- ✅ "Pierre Dupont" disparaît de la liste
- ✅ Dossier `face_samples/Pierre Dupont/` supprimé

---

## 10. Test de persistance des données

**Préconditions :**
- Plusieurs étudiants enregistrés avec transactions

**Étapes :**
1. Fermer l'application
2. Relancer l'application
3. Vérifier les données

**Résultats attendus :**
- ✅ Tous les comptes présents
- ✅ Soldes corrects
- ✅ Reconnaissance fonctionne toujours

---

## 📊 Résumé des Tests

| Test | Fonctionnalité | Statut |
|------|----------------|--------|
| 1 | Ajout étudiant | ⬜ |
| 2 | Reconnaissance OK | ⬜ |
| 3 | Personne inconnue | ⬜ |
| 4 | Débit automatique | ⬜ |
| 5 | Déjà débité | ⬜ |
| 6 | Débit manuel | ⬜ |
| 7 | Ajout crédit | ⬜ |
| 8 | Consultation comptes | ⬜ |
| 9 | Suppression | ⬜ |
| 10 | Persistance | ⬜ |

**Légende :**
- ⬜ Non testé
- ✅ Réussi
- ❌ Échoué

---

**Document créé pour le projet RecoFacial - Institut Limayrac BSI-DSN**
