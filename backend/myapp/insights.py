from .questions_data import INSIGHTS
import logging

logger = logging.getLogger(__name__)

class Insights:
    def __init__(self, answers_user1, answers_user2):
        """
        Inicializa a classe com as respostas dos usuários.
        :param answers_user1: Dict com as respostas do Usuário 1 (ex: {"Q7": "Carinho", ...})
        :param answers_user2: Dict com as respostas do Usuário 2
        """
        self.answers_user1 = answers_user1
        self.answers_user2 = answers_user2

    def generate_insights(self, user1_name="Usuário 1", user2_name="Usuário 2"):
        """
        Gera insights com base nas respostas e na configuração do INSIGHTS.
        :param user1_name: Nome do Usuário 1
        :param user2_name: Nome do Usuário 2
        :return: Lista de insights detalhados e scores individuais
        """
        insights_results = []
        user1_total_score = 0
        user2_total_score = 0

        for insight in INSIGHTS:
            insight_title = insight["title"]
            insight_category = insight["category"]
            insight_prefix = insight["prefix"]
            insight_suffix = insight["suffix"]
            questions = insight["Questions"]

            if len(questions) == 2:
                question1_id, question2_id = questions

                # Respostas dos usuários
                user1_answer_q1 = self.answers_user1.get(question1_id)
                user2_answer_q2 = self.answers_user2.get(question2_id)

                user2_answer_q1 = self.answers_user2.get(question1_id)
                user1_answer_q2 = self.answers_user1.get(question2_id)

                # Verificar alinhamentos cruzados
                user1_correct = user1_answer_q2 == user2_answer_q1
                user2_correct = user2_answer_q2 == user1_answer_q1

                # Atualizar scores individuais
                user1_score = 10 if user1_correct else 0
                user2_score = 10 if user2_correct else 0
                user1_total_score += user1_score
                user2_total_score += user2_score

                # Determinar cor do card
                color_flag = self._determine_color_flag(user1_correct, user2_correct)

                # Criar descrição
                description = self._create_description(
                    user1_name, user2_name,
                    insight_prefix, insight_suffix,
                    user1_answer_q2, user2_answer_q1,
                    user1_correct, user2_correct
                )

                insights_results.append({
                    "title": insight_title,
                    "description": description,
                    "category": insight_category,
                    "user1_score": user1_score,
                    "user2_score": user2_score,
                    "color_flag": color_flag
                })

        logger.info(f"Insights gerados para {user1_name} e {user2_name}")
        logger.info(f"Score {user1_name}: {user1_total_score}")
        logger.info(f"Score {user2_name}: {user2_total_score}")
        logger.info(insights_results)

        return {"insights": insights_results, "user1_total_score": user1_total_score, "user2_total_score": user2_total_score}

    @staticmethod
    def _determine_color_flag(user1_correct, user2_correct):
        if user1_correct and user2_correct:
            return "green"
        elif user1_correct or user2_correct:
            return "yellow"
        return "red"

    @staticmethod
    def _create_description(user1_name, user2_name, insight_prefix, insight_suffix,
                             user1_answer_q2, user2_answer_q1, user1_correct, user2_correct):
        description = (f"{user1_name} respondeu que {user2_name} {insight_prefix} '{user1_answer_q2}', enquanto "
                       f"{user2_name} respondeu que {insight_prefix} '{user2_answer_q1}'. ")

        if user1_correct and user2_correct:
            description += f"Ambos acertaram {insight_suffix} um do outro, o que mostra alinhamento."
        elif user1_correct:
            description += (f"{user1_name} está certo(a) sobre {insight_suffix} de {user2_name}, mas {user2_name} "
                            f"errou ao dizer que {user1_name} {insight_prefix} '{user2_answer_q1}'.")
        elif user2_correct:
            description += (f"{user2_name} está certo(a) sobre {insight_suffix} de {user1_name}, mas {user1_name} "
                            f"errou ao dizer que {user2_name} {insight_prefix} '{user1_answer_q2}'.")
        else:
            description += f"Ambos erraram ao identificar {insight_suffix} um do outro. Que tal conversarem sobre isso?"

        return description
