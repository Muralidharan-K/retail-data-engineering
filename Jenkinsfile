pipeline {
    agent any

    stages {

        stage('Jenkins Environment Check') {
            steps {
                bat 'whoami'
                bat 'git --version'
                bat 'D:/Projects/retail-data-engineering/.venv/Scripts/python.exe --version'
                bat 'D:/Projects/retail-data-engineering/.venv/Scripts/dbt.exe --version'
            }
        }

        stage('dbt Snowflake Connection') {
            steps {
                withCredentials([
                    string(
                        credentialsId: 'snowflake-password',
                        variable: 'SNOWFLAKE_PASSWORD'
                    )
                ]) {
                    bat '''
                        D:/Projects/retail-data-engineering/.venv/Scripts/dbt.exe debug ^
                        --project-dir D:/Projects/retail-data-engineering/retail_dbt ^
                        --profiles-dir D:/Projects/retail-data-engineering/jenkins_profiles
                    '''
                }
            }
        }

        stage('Python Data Quality') {
            steps {
                bat '''
                    D:/Projects/retail-data-engineering/.venv/Scripts/python.exe ^
                    D:/Projects/retail-data-engineering/python/validate_retail_data.py ^
                    --input D:/Projects/retail-data-engineering/data/raw/orders.csv ^
                    --fail-on-error
                '''
            }
        }

        stage('dbt Run') {
            steps {
                withCredentials([
                    string(
                        credentialsId: 'snowflake-password',
                        variable: 'SNOWFLAKE_PASSWORD'
                    )
                ]) {
                    bat '''
                        D:/Projects/retail-data-engineering/.venv/Scripts/dbt.exe run ^
                        --project-dir D:/Projects/retail-data-engineering/retail_dbt ^
                        --profiles-dir D:/Projects/retail-data-engineering/jenkins_profiles
                    '''
                }
            }
        }

        stage('dbt Test') {
            steps {
                withCredentials([
                    string(
                        credentialsId: 'snowflake-password',
                        variable: 'SNOWFLAKE_PASSWORD'
                    )
                ]) {
                    bat '''
                        D:/Projects/retail-data-engineering/.venv/Scripts/dbt.exe test ^
                        --project-dir D:/Projects/retail-data-engineering/retail_dbt ^
                        --profiles-dir D:/Projects/retail-data-engineering/jenkins_profiles
                    '''
                }
            }
        }
    }
}