import logging
from SapGuiLibrary import SapGuiLibrary
from dotenv import load_dotenv

from hnt_sap_gui.RPA_HNT_Constants import COD_LIBERACAO_BLOQUADO
from hnt_sap_gui.nota_fiscal.fatura_transaction import FaturaTransaction
from hnt_sap_gui.nota_fiscal.miro_transaction import MiroTransaction

from .common.session import sessionable
from .nota_fiscal.nota_pedido_transaction import NotaPedidoTransaction
from .nota_fiscal.liberacao_transaction import LiberacaoTransaction

logger = logging.getLogger(__name__)

class SapGui(SapGuiLibrary):
    def __init__(self) -> None:
        load_dotenv()
        pass

    @sessionable
    def hnt_run_transaction(self, data):
        logger.info(f"enter execute run_hnt_transactions data:{data}")
        tx_result_nota_pedido = NotaPedidoTransaction().execute(self, nota_pedido=data['nota_pedido'])
        tx_result_liberacao = LiberacaoTransaction().execute(self, tx_result_nota_pedido.codigo)
        results = {
            "nota_pedido": tx_result_nota_pedido,
            "liberacao": tx_result_liberacao
        }
        if COD_LIBERACAO_BLOQUADO == tx_result_liberacao.codigo:
            logger.info(f"leave execute run_hnt_transactions result:{', '.join([str(results[obj]) for obj in results])}")
            return results
        
        results['miro'] = MiroTransaction().execute(self, data=data["miro"], numero_pedido=tx_result_nota_pedido.codigo)
        logger.info(f"leave execute run_hnt_transactions result:{', '.join([str(results[obj]) for obj in results])}")
        
        return results

    @sessionable
    def hnt_run_transaction_miro(self, numero_pedido, data):
        logger.info(f"enter execute hnt_run_transaction_miro data:{data}")
        tx_result_liberacao = LiberacaoTransaction().execute(self, numero_pedido)
        results = {
            "liberacao": tx_result_liberacao,
            "miro": None
        }
        if COD_LIBERACAO_BLOQUADO == tx_result_liberacao.codigo:
            logger.info(f"leave execute hnt_run_transaction_miro result:{', '.join([str(results[obj]) for obj in results])}")
            return results
        
        results['miro'] = MiroTransaction().execute(self, data, numero_pedido)
        logger.info(f"leave execute hnt_run_transaction_miro result:{', '.join([str(results[obj]) for obj in results])}")
        return results

    @sessionable
    def hnt_run_transaction_FV60(self, data):
        result = FaturaTransaction().execute(self, data)
        logger.info(f"leave execute hnt_run_transaction_FV60 result: '{result}'")
        return result
