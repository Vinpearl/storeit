# iOS - Android - Web

_Les deux clients mobiles et le client web, bien qu'étant différents au niveau de l'interface utilisateur, possèdent les mêmes fonctionnalités et bénéficieront des mêmes tests lors des scénarios de démonstration._

### Scénarios de démonstration

__1. Connexion du client__

L'utilisateur peut se connecter à l'application grâce à son compte Google ou Facebook. Il dispose d'un écran de connexion avec un bouton pour chaque type de connexion. C'est une connexion de type OAuth, c'est-à-dire que nous recevons un token de la part de Google et Facebook que nous utilisons ensuite pour l'authentification avec notre serveur.

__Les tests suivants seront réalisés pour les deux plateformes :__
- Connexion avec le bouton "Google".
- Connexion avec le bouton "Facebook".
- Vérification de la persistence de la session de connexion : après redémarrage de l'appareil ou du simulateur, l'utilisateur doit rester connecté.

__2. Exploration du dossier synchronisé StoreIt__

Après s'être connecté, l'utilisateur arrive sur une vue representant son dossier synchronisé StoreIt. Les dossiers et fichiers qu'il contient y sont présents; par défaut en forme de liste, ou bien en mosaïque. L'utilisateur peut parcourir son dossier synchronisé simplement en selectionnant par exemple un sous-dossier. Il peut aussi selectionner un fichier, par exemple une image, afin d'en obtenir un aperçu.

__Les tests suivants seront réalisés pour les deux plateformes :__
- Après la connexion, il sera vérifié que les fichiers et dossiers synchronisés sont présents en forme de liste.
- Affichage du contenu synchronisé en mosaïque.
- Exploration du contenu : parcourir des sous-dossiers et obtenir l'aperçu de fichiers.

__3. Menu contextuel d'un élément__

Chaque élément (fichiers ou dossiers) possède un menu contextuel, accessible via un bouton, qui permet d'effectuer des actions en fonction du type de l'élément. En règle générale, il sera possible de réorganiser le dossier synchronisé grâce à des déplacements ou supressions d'éléments. De plus, les fichiers bénéficieront d'une option de téléchargement.

__Les tests suivants seront réalisés pour les deux plateformes :__
- Suppression d'un fichier.
- Déplacement d'un fichier dans un dossier.
- Suppression d'un dossier.
- Téléchargement d'un fichier et vérification de sa présence sur l'appareil : téléchargement d'une photo, et vérification de la présence de celle-ci dans la mémoire de l'appareil.

__4. Importation de fichiers__

L'utilisateur possède un bouton permettant d'importer des fichiers. Par exemple, il peut importer une photo présente sur son appareil ou prendre une photo grâce à celui-ci pour l'importer directement.

__Les tests suivants seront réalisés pour les deux plateformes :__
- Importer une photo présente sur l'appareil.
- Importer immédiatement une photo prise grâce à l'appareil photo (Android/iOS).
