#include <stdio.h>
#include <string.h>

// Função para analisar o sentimento do texto
int emotions_analysis_c(const char *text) {
    int positive_words = 0;
    int negative_words = 0;

    // Lista de palavras positivas e negativas (simplificadas)
    const char *positive_words_list[] = {"bom", "feliz", "ótimo", "excelente"};
    const char *negative_words_list[] = {"ruim", "triste", "terrível", "horrível"};

    // Verifica cada palavra no texto
    char *token = strtok((char *)text, " ");
    while (token != NULL) {
        // Verifica se a palavra está na lista de palavras positivas
        for (int i = 0; i < sizeof(positive_words_list) / sizeof(positive_words_list[0]); i++) {
            if (strcmp(token, positive_words_list[i]) == 0) {
                positive_words++;
                break;
            }
        }
        // Verifica se a palavra está na lista de palavras negativas
        for (int i = 0; i < sizeof(negative_words_list) / sizeof(negative_words_list[0]); i++) {
            if (strcmp(token, negative_words_list[i]) == 0) {
                negative_words++;
                break;
            }
        }
        token = strtok(NULL, " ");
    }

    // Retorna o resultado da análise de sentimento
    if (positive_words > negative_words) {
        return 1; // Sentimento positivo
    } else if (positive_words < negative_words) {
        return -1; // Sentimento negativo
    } else {
        return 0; // Sentimento neutro
    }
}
