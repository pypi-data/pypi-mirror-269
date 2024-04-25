import requests
import json

class Request:
    def __init__(self, url, token):
        self.url = url
        self.token = token

    def _get_request(self, endpoint, params=None):
        headers = {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer ' + self.token
        }
        try:
            response = requests.get(endpoint, headers=headers, params=params, timeout=10) # 10초 타임아웃 설정
            response.raise_for_status()  # HTTPError 예외 발생 시키기
            return response.json()
        except requests.exceptions.HTTPError as e:
            print(f"HTTP 에러 발생: {e.response.status_code} - {e.response.text}")
        except requests.exceptions.ConnectionError:
            print("서버에 연결할 수 없습니다.")
        except requests.exceptions.Timeout:
            print("요청 시간 초과.")
        except requests.exceptions.RequestException as e:
            print(f"요청 실패: {e}")
        except json.decoder.JSONDecodeError:
            print("JSON 디코딩 오류: 응답이 유효한 JSON 형식이 아닙니다."+response.text)
        except Exception as e:
            print(f"알 수 없는 오류 발생: {e}")
        
    def _post_request(self, endpoint, data=None):
        headers = {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer ' + self.token
        }
        try:
            response = requests.post(endpoint, json=data, timeout=10) # 10초 타임아웃 설정
            response.raise_for_status()  # HTTPError 예외 발생 시키기
            return response.json()
        except requests.exceptions.HTTPError as e:
            print(f"HTTP 에러 발생: {e.response.status_code} - {e.response.text}")
        except requests.exceptions.ConnectionError:
            print("서버에 연결할 수 없습니다.")
        except requests.exceptions.Timeout:
            print("요청 시간 초과.")
        except requests.exceptions.RequestException as e:
            print(f"요청 실패: {e}")
        except json.decoder.JSONDecodeError:
            print("JSON 디코딩 오류: 응답이 유효한 JSON 형식이 아닙니다."+response.text)
        except Exception as e:
            print(f"알 수 없는 오류 발생: {e}")
