# -*- coding: utf-8 -*-

class Language():
    pass

#EN = Language()
IT = Language()

# --- IT Statements --- #
    # Text message
IT.Start = "Hey, Netflixers! 😎\nCon chi di voi $$ condivide l'account? 👇"
IT.UseThis = "⚠️ Una procedura di configurazione è già attiva, usa questo messaggio. ☝️\n\nSe è stato accidentalmente eliminato, ricomincia la configurazione premendo qui 👇"
IT.ConfirmList = "Confermi la lista di partecipanti?"
IT.Schedule = "📆 In che *giorno del mese* viene rinnovato il tuo abbonamento?"
IT.ConfirmSchedule = "Confermi che il tuo abbonamento a Netflix viene rinnovato il giorno *$$*?"
IT.Done = "Finito! Quindi...\n\n🎬 I Netflixers sono:\n*$$*\n📆 L'abbonamento si rinnova il *$$* di ogni mese.\n🔔 Le notifiche sono *attive*.\n\nBuona visione! 😎"
IT.TimeToPay = "📢 Un altro mese è passato, per poter continuare a guardare tutte le serie TV su Netflix è necessario pagare la propria parte.\n\nSono *$$€ a testa*. 💸"
IT.EveryonePaid = "Tutti hanno pagato la propria parte! Prossimo appuntamento il *$$*.\n\n*Buon Netflix!* 😎"
IT.AlreadyConfigured = "Le impostazioni per questo gruppo sono già state confermate oppure una procedura di configurazione è in corso. Se hai bisogno di ripartire da zero, premi sotto"
IT.NewConfig = "Per riconfigurare il gruppo, premi 👉 /start"
IT.ConfirmReset = "Sicuro di voler resettare le impostazioni? *Questa azione è irreversibile.*"
IT.PaymentAccepted = "Il pagamento di $$ è stato *accettato*! ✅"
    # Callback query
IT.MaxReached = "⚠️ E' già stato raggiunto il numero massimo di partecipanti (4)!"
IT.AlreadySigned = "Sei già un Netflixers! 😎\nSe hai premuto per sbaglio oppure hai cambiato idea, puoi cancellarti dalla lista facendo un tap sul tuo nome."
IT.AtLeastOneUser = "⚠️ E' necessario almeno un partecipante per andare avanti."
IT.NotAdmin = "Non sei tu l'amministratore, mi dispiace. 🙁"
IT.AlreadyPayed = '$$ ha già pagato! 💰'
IT.Resetted = 'Le impostazioni del gruppo sono state resettate con successo! ✅'
IT.NotPermitted = '️⚠️ Azione non permessa.'
IT.Added = "Aggiunto ✅"
IT.Removed = "Rimosso ✅"
IT.IsWaiting = "⚠️ Sei già in attesa di conferma."
IT.WaitingFor = "⏳ Attendi la conferma dell'avvenuto pagamento da parte dell'amministratore."
IT.AlmostDone = "⏳ Ci siamo quasi..."
    # Private Chat Statements
IT.Welcome = ("Ciao *$$*! Io sono un bot, e ti aiuterò a gestire il tuo gruppo Netflix. 😊\n\n"
             "Prima di cominciare devi sapere che sono ancora in uno stadio di sviluppo _alpha_, potrebbero quindi verificarsi comportamenti non previsti. "
             "Se riscontri qualche tipo di problema, o per qualsiasi altra cosa, ti invito a contattare il mio programmatore @LinkOut, sarà lieto di aiutarti. "
             "Se sei un programmatore anche tu puoi trovarmi su [GitHub](https://github.com/xLinkOut/cagateisoldibot).\n\n"
             "Ecco qualche informazione utile: per funzionare, aggiungimi in un gruppo usando il nickname @cagateisoldibot. "
             "Il primo step sarà quello di 📝 segnare tutte le persone che condividono Netlifx con te, poi seguirà una velocissima configurazione dove potrai indicare il 📆 giorno del mese in cui l'abbonamento si rinnova. "
             "In quel giorno, ogni mese, manderò una notifica con una lista dove le persone che hanno pagato potranno segnarsi, e dove poi tu dovrai confermare il pagamento.\n\n"
             "*That's it!* Nuove funzioni sono in sviluppo e arriveranno presto. Questo progetto è completamente gratuito, ma i server costano; se sei interessato a partecipare trovi il tasto 🎁 Dona nella tastiera in basso.")
IT.Donate = "Per supportare il progetto puoi donare tramite PayPal a [questa pagina](https://paypal.me/LCirillo). ❤️"
IT.About = "Made with ❤️ and a lot of </code> by @LinkOut. 👨‍💻"