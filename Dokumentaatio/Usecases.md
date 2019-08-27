### Use cases

+ Users will have the ability to sell and buy action from other users. 
+ Users will have the ability to register and login to the site. 
+ Users will only see tournaments on the tournament-selling page where they are not the seller since you cannot buy action from your own tournaments.
+ users will see tournaments where they are selling action for and who has bought action from them, they will also see and who they have bought action from.
+ admin will see the statistics of top buyers and sellers.



### SQL queries


Find tournaments where you are not the seller:
```
SELECT * FROM tournament_package LEFT JOIN account on tournament_package.account_id = account.id
WHERE NOT account.id = current_user.id;
```

Find tournaments you have bought action from:
```
SELECT bought_action_from_tournament.seller_name, tournament_package.tournament, tournament_package.buyIn, bought_action_from_tournament.actionboughtpct FROM account 
LEFT JOIN bought_action_from_tournament ON account.id = bought_action_from_tournament.buyer_id
LEFT JOIN tournament_package ON bought_action_from_tournament.tournament_package_id = tournament_package.id
WHERE bought_action_from_tournament.buyer_id = current_user.id;
```

Find tournaments you have sold action for:
```
SELECT tournament, buyin, pcttobesold, pctleft, tournament_package.id FROM tournament_package
LEFT join account ON tournament_package.account_id = account.id 
WHERE account_id = current_user.id;
```

Find all the share buyers for certain tournament:
```
SELECT buyer_id, actionboughtpct, account.name from bought_action_from_tournament 
LEFT JOIN account ON buyer_id = account.id
WHERE bought_action_from_tournament.tournament_package_id = Some tournament id;
```

Find the users who have bought most shares across all tournaments:
```
SELECT count(buyer_id), account.name FROM bought_action_from_tournament
LEFT JOIN account ON bought_action_from_tournament.buyer_id = account.id
GROUP BY account.name
```


Find the users who have most tournaments up for sale:
```
SELECT COUNT(account.id), account.name FROM tournament_package
LEFT JOIN account ON tournament_package.account_id = account.id
GROUP BY account.name
```
