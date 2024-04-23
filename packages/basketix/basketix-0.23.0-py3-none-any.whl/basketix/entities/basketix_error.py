"""Basketix error module"""

import os
import traceback
from typing import Optional

from .language import DEFAULT_LANGUAGE

ENVIRONMENT = os.getenv("ENVIRONMENT", "test")


class BasketixError(Exception):
    """Basketix error class"""

    ERROR_MESSAGES = {
        "UnknownError": {
            "en": "Unknown error",
            "fr": "Erreur inconnue",
        },
        "Unauthorized": {
            "en": "Not authorized",
            "fr": "Non autorisé",
        },
        "InvalidParameters": {
            "en": "Invalid parameters : { parameters_error }",
            "fr": "Paramètres non valides : { parameters_error }",
        },
        "NotFreeAgent": {
            "en": "The player is not a free agent",
            "fr": "Le joueur n'est pas un agent libre",
        },
        "InvalidBid_TooSmall": {
            "en": "Player is more expensive ({ player_cost } M$) than your bid ({ cost } M$)",
            "fr": "Le joueur est plus cher ({ player_cost } M$) que votre offre ({ cost } M$)",
        },
        "InvalidBid_CutRecently": {
            "en": "You cut the player for less than { min_days_after_cut } days",
            "fr": "Vous avez coupé le joueur il y a moins de { min_days_after_cut } jours",
        },
        "InvalidBid_CapSpace": {
            "en": "You do not have enough cap space ({ cap_space } M$) for this bid ({ cost } M$)",
            "fr": "Vous n'avez pas assez de cap space ({ cap_space } M$) pour cette offre ({ cost } M$)",
        },
        "InvalidBid_LowerThanPrevious": {
            "en": "Your new bid must be higher than the previous one: { old_bid_cost } M$",
            "fr": "Votre nouvelle offre doit être supérieure à l'ancienne : { old_bid_cost }  M$",
        },
        "InvalidWithdraw": {
            "en": "You have not bid for this player",
            "fr": "Vous n'avez pas enchéri pour ce joueur",
        },
        "InvalidOwner": {
            "en": "You do not own the player",
            "fr": "Vous n'êtes pas propriétaire du joueur",
        },
        "InvalidPickDelay": {
            "en": "The draft pick delay should be at least { min_delay } seconds.",
            "fr": "Le délai de sélection doit être d'au moins { min_delay } secondes.",
        },
        "AlreadyInLeague": {
            "en": "You are already in the league",
            "fr": "Vous êtes déjà dans la ligue",
        },
        "AccessToLeagueDenied": {
            "en": "Access to the league denied",
            "fr": "Accès à la ligue refusé",
        },
        "UnknownDraftType": {
            "en": "Unknown draft type",
            "fr": "Type de draft inconnu",
        },
        "InvalidPickNumber": {
            "en": "Pick number { pick_number} is not your pick",
            "fr": "Le choix numéro { pick_number} n'est pas votre choix",
        },
        "AlreadyDrafted": {
            "en": "Some players have already been drafted",
            "fr": "Certains joueurs ont déjà été draftés",
        },
        "CanNotPick": {
            "en": "You can not pick the player",
            "fr": "Vous ne pouvez pas sélectionner le joueur",
        },
        "InvalidSeason": {
            "en": "Can not get season",
            "fr": "Impossible d'obtenir la saison",
        },
        "TeamAlreadyExists": {
            "en": "A team already exists",
            "fr": "A team already exists",
        },
        "InvalidPositionsTeam": {
            "en": "Player positions not allowed to form a team",
            "fr": "Les positions des joueurs ne sont pas autorisées à former une équipe",
        },
        "InvalidEmail": {
            "en": "{ email } already used",
            "fr": "{ email } déjà utilisée",
        },
        "InvalidConfirmationCode": {
            "en": "Confirmation code is not valid",
            "fr": "Confirmation code n'est pas valide",
        },
        "PlayerWithoutCost": {
            "en": "Player { player_id } does not have a cost",
            "fr": "Le joueur { player_id } n'a pas de coût",
        },
        "InvalidEmailFormat": {
            "en": "Invalid email format",
            "fr": "Format d'email invalide",
        },
        "InvalidPasswordFormat": {
            "en": "Invalid password policy",
            "fr": "Politique de mot de passe invalide",
        },
        "InvalidPasswordConfirmation": {
            "en": "Non-identical passwords",
            "fr": "Les mots de passe ne sont pas identiques",
        },
        "NotLeagueMember": {
            "en": "You are not a member of this league",
            "fr": "Vous n'êtes pas membre de cette ligue",
        },
        "NotFinishedSeason": {
            "en": "At least one season not completed",
            "fr": "Au moins une saison non terminée",
        },
        "StartedWeek": {
            "en": "This week began",
            "fr": "Cette semaine a commencé",
        },
        "NotInRoster": {
            "en": "Some players are not in your roster",
            "fr": "Certains joueurs ne font pas partie de votre effectif",
        },
        "FinishedDraft": {
            "en": "Draft is finished: no free agents found",
            "fr": "La draft est terminée : aucun agent libre n'a été trouvé",
        },
        "PlayerMustHaveOnePosition": {
            "en": "A player can have only one position",
            "fr": "Un joueur ne peut avoir qu'une seule position",
        },
        "InvalidPointsTable": {
            "en": "Invalid points table",
            "fr": "Tableau de points invalide",
        },
        "TooExpansiveTeam": {
            "en": "Team is too expansive: { cost } > { limit }",
            "fr": "L'équipe est trop cher : { cost } > { limit }",
        },
    }

    def __init__(
        self,
        error_code: str,
        tokens: Optional[dict] = None,
        inner_exception: Optional[Exception] = None,
        status_code=400,
    ):
        """Init the basketix error."""
        Exception.__init__(self)
        self.error_code = error_code
        self.error_message = None
        self.tokens: dict = tokens if tokens else {}
        self.status_code = status_code
        self._inner_exception = inner_exception

    def __str__(self):
        msg = f"BasketixError : {self.error_code}"
        if self._inner_exception is not None:
            trb = "\n".join(
                traceback.format_exception(
                    self._inner_exception.__class__, self._inner_exception, self._inner_exception.__traceback__
                )
            )
            msg = msg + "\n" + trb
        return msg

    def get(self, language: Optional[str]) -> dict:
        error = {
            "type": "BasketixError",
            "code": self.error_code,
            "message": self._error_message(language),
        }
        if ENVIRONMENT != "prod":
            error["traceback"] = str(self)

        return error

    def _error_message(self, language: Optional[str]) -> str:
        language = language if language else DEFAULT_LANGUAGE
        messages = self.ERROR_MESSAGES[self.error_code]
        message = messages[language] if language in messages else messages[DEFAULT_LANGUAGE]

        for key, value in self.tokens.items():
            message = message.replace(f"{{ {key} }}", str(value))

        return message
