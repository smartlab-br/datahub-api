''' Repository para recuperar informações da CEE '''
import json

from model.base import BaseModel
from repository.thematic import ThematicRepository

#pylint: disable=R0903
class MigracoesEscravo(BaseModel):
    ''' Definição do repo '''
    METADATA = {
        'fonte': 'Ministério da Economia - Secretaria de Trabalho', 'link': 'http://trabalho.gov.br/'
    }

    def __init__(self):
        ''' Construtor '''
        self.repo = ThematicRepository()
        self.sankey_ds = None

    def get_repo(self):
        ''' Garantia de que o repo estará carregado '''
        if self.repo is None:
            self.repo = ThematicRepository()
        return self.repo

    def find_dataset_sankey(self, options=None):
        options['no_wrap'] = True
        options['theme'] = 'migracoesescravos'
        dataset = super().find_dataset(options)
        self.sankey_ds = dataset.to_dict('records')

        snk_nodes = []
        snk_links = []
        if (self.sankey_ds is not None and len(self.sankey_ds) > 0):
            nu_data = self.sankey_ds.pop(0)
            (snk_nodes, snk_links) = self.traverse(
                nu_data,
                [nu_data['source']],
                [nu_data['source']],
                []
            )

        metadata = self.fetch_metadata()
        metadata["sankey_data"] = {
            "nodes": snk_nodes,
            "links": snk_links
        }

        # Wraps and returns
        if dataset is None:
            return None
        if options is not None:
            if 'as_pandas' in options and options['as_pandas']:
                return {
                    "metadata": metadata,
                    "dataset": dataset,
                }
            elif 'as_dict' in options and options['as_dict']:
                return {
                    "metadata": metadata,
                    "dataset": dataset.to_dict('records'),
                }
        return f'{{ \
            "metadata": {json.dumps(metadata)}, \
            "dataset": {dataset.to_json(orient="records")} \
            }}'

    def traverse(self, current_data=None, past_path=[], nodes=[], links=[]):
        ''' Builds links and nodes for sankey network '''
        # Se a lista de nós está vazia, é o início da recursividade
        if current_data["target"] in past_path or self.is_circular_added_link(current_data["target"], past_path.copy(), links.copy()):
            # Se o target já estiver no caminho percorrido, é circular.
            # Se, alternativamente, formar um caminho circular com os links
            # ja percorridos.
            # Então, muda a referência do nó para Nome + "'"
            # Verifica se o novo nome já está no rol de nodes
            mod_data = current_data.copy()
            mod_data['target'] = current_data['target'] + "'"
            if mod_data['target'] in nodes:
                # Se já existe, checar se é referência circular
                (nodes, links) = self.traverse(mod_data, past_path, nodes, links)
            else:
                # Não existindo, cria novo nó e adiciona o link
                nodes.append(mod_data['target'])
                links.append(mod_data)
        else: # Não sendo referência circular, adiciona o nó (se já não existir na lista nodes) e o link
            # Não existindo, cria novo nó e adiciona o link
            if not current_data['target'] in nodes:
                nodes.append(current_data['target'])
            links.append(current_data)
        # Segue o path, incrementando itens
        # Localiza novo nó na cadeia
        dead_end = True
        for indx, next_data in enumerate(self.sankey_ds):
            if next_data['source'] == current_data["target"]:
                # Invoca a recursividade, com o próximo nó no caminho
                dead_end = False
                nu_past_path = past_path.copy()
                nu_past_path.append(next_data["target"])
                next_data = self.sankey_ds.pop(indx)
                if next_data["source"] not in nodes:
                    nodes.append(next_data["source"])
                (nodes, links) = self.traverse(next_data, nu_past_path, nodes, links)
        while dead_end and len(past_path) == 1 and len(self.sankey_ds) > 0:
            # Se não encontrou mais itens no caminho e a iteração
            # corrente for o início de um caminho, inicia um novo
            # caminho, faz o traverse para um novo item do dataset.
            nu_data = self.sankey_ds.pop(0)
            if nu_data["source"] not in nodes:
                nodes.append(nu_data["source"])
            (nodes, links) = self.traverse(nu_data, [nu_data['source']], nodes, links)
        return (nodes, links)

    def is_circular_added_link(self, next_target, past_path, links):
        ''' Checks if there's a circular path with previous links '''
        if next_target in past_path:
            return True
        past_path.append(next_target)
        for link in links:
            if (link["source"] == next_target and
                self.is_circular_added_link(link["target"], past_path, links)):
                return True
        return False
