from dataclasses import dataclass
import jwt


@dataclass
class LolaToken:
    tenantId: str
    assistantId: str


def decode_lola_token(token) -> LolaToken:
    options={"verify_signature": False}
    # decode token without verifying signature
    decoded = jwt.decode(token, algorithms=['HS256'], options=options)
    data = decoded['data']
    tenantId = data['tenantId']
    assistantId = data['assistantId']

    return LolaToken(tenantId, assistantId)


# if __name__ == "__main__":

