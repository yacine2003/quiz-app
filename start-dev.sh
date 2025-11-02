#!/bin/bash
# Script pour démarrer les serveurs de développement

echo "🚀 Démarrage des serveurs de développement..."

# Arrêter les processus existants
echo "🛑 Arrêt des processus existants..."
lsof -ti:5001 | xargs kill -9 2>/dev/null
lsof -ti:3000 | xargs kill -9 2>/dev/null
sleep 2

# Activer le virtualenv
cd "$(dirname "$0")"
source venv/bin/activate

# Démarrer le backend Flask
echo "🔧 Démarrage du backend Flask sur http://localhost:5001"
cd quiz-api
python app_new.py > /tmp/quiz-api.log 2>&1 &
BACKEND_PID=$!
echo "   Backend PID: $BACKEND_PID"

# Attendre que le backend soit prêt
sleep 3

# Vérifier que le backend répond
if curl -s http://localhost:5001/health > /dev/null; then
    echo "✅ Backend démarré avec succès"
else
    echo "❌ Erreur: Le backend ne répond pas"
    cat /tmp/quiz-api.log
    exit 1
fi

# Démarrer le frontend Vite
echo "🎨 Démarrage du frontend Vite sur http://localhost:3000"
cd ../quiz-ui
npm run dev > /tmp/quiz-ui.log 2>&1 &
FRONTEND_PID=$!
echo "   Frontend PID: $FRONTEND_PID"

sleep 3

echo ""
echo "✨ Serveurs démarrés !"
echo ""
echo "📍 URLs:"
echo "   Frontend: http://localhost:3000"
echo "   Backend:  http://localhost:5001"
echo ""
echo "📋 Pour arrêter les serveurs:"
echo "   kill $BACKEND_PID $FRONTEND_PID"
echo ""
echo "📊 Logs:"
echo "   Backend:  tail -f /tmp/quiz-api.log"
echo "   Frontend: tail -f /tmp/quiz-ui.log"
echo ""

