# projet_invicible_pacman Python3

	## Class Map

		Notre classe map est celle qui modelise notre map, les maps doivent être de 20 / 20 dans un fichier .txt
		20 / 20 car parfois nous utilisons la height de notre tableau pour en déduire la width, parfois nous mettons 20 directement
		Une revue du code, pour mettre la height de la map en argument dans chaque fonction qui en ont besoin
		est a faire, aini la map pourra être rectangle par exemple.

		Elle contient aussi notre Pacman, notre model de food map, elle initialise notre groupe de phantome et les ajoutes dans un groupe

		Elle sert aussi de classe principale pour lancer les updates et les draw de chacun de ces éléments

		Le controle du pacman se fait via les fleches du clavier
		afin de lancer l'ia naive de pacman il faut décommenter la ligne 66 de map.py, commenter la 67
		commenter la 118 et décommenter la 120

	
	## Best first search (avec distance de tchebychev) + distance dans un plan cartésien

		Le fichier bfs comme son nom l'indique contient notre algorithme best first search , implémenté de manière itérative
		La facon récursive du BFS contient le même nombre d'itération bien que plus légère en terme de mémoire

		De plus la class BFS_cheby contient une fonction Distance qui renvoie la distance entre deux points (x1,y1) et (x2, y2) sur un plan cartésien
		cette fonction nous sert notemment dans notre BFS ( cas des téléportations )

		
	## Pacman
		### Class Pacman
			
			Cette classe est hérité de la classe PygameSprite ce qui nous permet de draw notre pacman via une image,  le déplacer via ces positions x et y 
			sa fonction update2 permet au joueur de controler notre Pacman

		### Class IAPacmanHungry

			Classe en construction qui n'a pas était finit car pas d'intéret spécial pour le rendu projet sur le même princie que IAPhantom qui permettrai de se
			déplacer selon la nourriture restante
			

		### Class IANaive

			C'est une IA hérité de Pacman qui fait que pacman se déplace de maniere aléatoire dans la map, ainsi Pacman change de direction a chaque intersections rencontrés (un angle, ou un noeud ayant 3 neouds libres autour de lui)

	
	## Les groupes de fantomes ( group_Ghost.py )
		### Class GroupGhost
			
			Cette classe permet simplement d'update les fantomes, ils sont tous indépendants les uns des autres
			si un voit pacman, il commence alors une course poursuite avec ce derniere grace a l'algo BFS sans avertir ces camarades
		
		### Class EnsembleOnEstPlusFort

			Cette classe est dans le même principe que la class GroupGhost mais à l'inverse de cette derniere, lorsqu'un fantome apercoit Pacman
			Tous les fantomes sont alors alerter de la position de Pacman est commencent tous indépendemment une course poursuite vers ce derniers 
		
		### Class EnsembleOnEstPlusFortV2
			
			Dans cette classe, si un fantome  apercoit Pacman alors il poursuit Pacman via BFS, ces coequipiers quant à eux entament un BFS vers les 
			intersections les plus proches de Pacman. pour une liste de x intersection : [(x1, y1), (x2,y2), ...] classés dans l'ordre croissant de distance
			entre l'intersection et Pacman, ces intersection sont triés dans l'ordre de distance avec Pacman afin de mettre en priorité les cases les plus proches
			de notre cible, ainsi le fantomes le plus proches de l'intersection la plus proche de pacman aura pour cible cette intersection, on choisit alors le fantome
			le plus proche de la seconde intersection etc etc  il y'a donc  n-1 intersections autour de pacman qui sont ciblés par les fantomes (nos n fantomes)
		
		### Class EnsembleOnEstPlusFortV3

			Cette classe a le même principe de fonctionnement que EnsembleOnEstPlusFortV2, cependant a l'instar de cette derniere ce ne sont pas les intersections les
			plus proches qui sont mises en priorité mais les extrémitées du chemin dans lequel pacman se trouve, on considère dans le cas d'un labirynthe de pacman
			que les fins de chemins sont situés ou pour chaque chaque Nodes du chemin, si il existe 3 cases vides alors c'est une intersection un chemin quand a lui
			a chacun de ces noeuds avec au plus 2 noeuds qui ne sont pas des murs autour de lui. Puis si toutes les extrémitées sont prises mais qu'il reste des fantomes
			qui n'ont pas étaient assignés, on part sur le même principe que la version précédentes, ils sont automatiquement dirigés vers les plus proches des intersections
			cette classe assigne donc un fantome qui pourchasse fantome et les autres aux intersections les plus proches de Pacman en mettant en priorité les 
			extrémités du chemin dans lequel PacMan se trouve

			Dans le cas ou les fantomes n'ont pas de cible ils parcourent la map via des BFS selon une mémoire de groupe (qui correspond à l'emplacement de 
			chaque pac-gum), a l'inverse des autres groupes qui les rend aléatoires.
			Donc a chaque itérations, si pacman n'a pas était détecté, les phantomes visitent des points ou la nourriture de pacman est censé se trouvé,
			si il passe par une case et voit que pacman l'a déjà manger, alors il le communique aux autres et plus aucun n'aura pour cible cette case
			Ainsi dans le cas ou il ne reste qu'une partie de la map, les phantomes ne seront pas dispersés dans toute la map si ils ont déjà fait le tour et observer
			que Pacman a tout manger, nous avons mis cette fonctionnalité en place afin d'etre au plus proche d'un comportement humain, car l'objectif principal de 
			Pacman sont les pac gums




	
	## Les fantomes
		### Class Ghost
			Cette la classe par défaut qui initialise un phantome qui hérite de la classe de Pygame.Sprite
			Un phantome par ne dispose pas de update il est juste drawable mais il dispose de plusieurs attributs utilisés dans ces classes filles
		
		### Class IAPhantomNaive
		
			Comme son nom l'indique c'et une IA qui fait les fantomes se déplacer de maniere aléatoire, ainsi il changent de direction a chaque fois qu'ils
			recontre une intersection ou se trouve dans un corner

		### Class IAPhantomBFS
			
			C'est la premiere version de l'IA du fantome qui permet au phantome de détecter pacman si il se trouve dans son champ de vision et ainsi d'initialiser
			et suivre un chemin généré via BFS, un phantome ne peut détecter Pacman que  si il avance vers ce dernier, le fait que Pacman et lui même soit sur la 
			même ligne ne permet pas au fantome de le détecter, un humain tournant le dos a un autre ne le voit pas par définition, si le fantome n'a pas de pacman
			en visue alors il utilise le update de sa classe mere IAPhantomNaive

		### Class IAPhantomBFS2

			class test mais même classe que IAPhantomBFS
		
		### Class IAPhantomBFS3

			Même principe que les deux dernieres cependant, lorsque l'ia n'a pas de pacman en visu s'en suit alors la méthodologie via leur carte de nourriture
			expliqué dans la section, EnsembleOnEstPlusFortV3

		
		### Class IAPhantom
			C'est la classe qui permet d'adopter le comportement de visite de la map selon la nourriture.

	## L'écran de défaite

		Si le joueur est attrapé par des fantomes, une fenetre clickable avec un message s'affiche indiquant au joueur qu'il a perdu 
		grace aux classes MessageBox et UTTextButton se trouvant dans end_window.py
	
	## Les fichiers de génération des niveaux

		Fichier  .txt qui comme dit précédemment contient les modeles de nos maps
		en 20 x 20
		Pacman étant représenté par la lettre 'p', les fantomes par g G h H , les murs par le signe '=' et la nourriture via le signe '.'

	### N.B : Dans le cadre de test, la fonction de collision ainsi que l'écran d'affichage de défaite ont été désactivés




	#Les axes d'améliorations

		Gérer le RATE d'updates par secondes, sur mon ordinateur le programme s'éxécute a une rapidité normal, mais sur celui de Fabio par exemple
		le jeu va beaucoup plus vite, donc réguler le nombre d'update par secondes

		Utiliser les fonctions "natives" du module Pygame, en effet le peu de temps que nous avons car ce cour c'est fait sur 5 séances nous a ammené
		à faire un mélange entre les fonctions natives de pygame et de la "tambouille maison" via les pos (x, y), il est possible que nous puissions
		utilisé des fonctions plus natives


		Debuger le continuer chemin ( Un fantome peut bugger quand il suit son parcours via son attribut tab_chemin ) 

		Imaginer et implémenté des IA pour Pacman, essayer de trouver des idées pour aller plus loin dan l'IA des fantomes
